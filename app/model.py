import torch
import torch.nn.functional as F
from dotenv import load_dotenv
import os
from transformers import CLIPModel, CLIPProcessor
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter

from app.config import (
    NORMAL_STATES,
    DEFECT_STATES,
    TEMPLATES
)

# ==========================
# Chargement configuration
# ==========================

load_dotenv()

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "openai/clip-vit-base-patch32"
)

DEFAULT_ANOMALY_THRESHOLD = 0.75

ANOMALY_THRESHOLD = float(
    os.getenv(
        "ANOMALY_THRESHOLD",
        DEFAULT_ANOMALY_THRESHOLD
    )
)

HF_TOKEN = os.getenv(
    "HF_TOKEN"
)


# ==========================
# Configuration du modèle
# ==========================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

WINDOW_SIZE = (224, 224)
STRIDE = 56


# ==========================
# Chargement du modèle
# ==========================

print(f"Chargement de CLIP sur {DEVICE}...")

model = CLIPModel.from_pretrained(
    MODEL_NAME,
    token=HF_TOKEN
)

processor = CLIPProcessor.from_pretrained(
    MODEL_NAME,
    token=HF_TOKEN
)

model.to(DEVICE)
model.eval()

print("Modèle CLIP chargé avec succès")


# ==========================
# Création des embeddings texte
# ==========================

def encode_text(category):
    """
    Création des représentations texte
    pour les états conforme et défaut.
    """

    normal_prompts = [
        template.format(f"{state} {category}")
        for state in NORMAL_STATES
        for template in TEMPLATES
    ]

    defect_prompts = [
        template.format(f"{state} {category}")
        for state in DEFECT_STATES
        for template in TEMPLATES
    ]

    prompts = normal_prompts + defect_prompts

    inputs = processor(
        text=prompts,
        return_tensors="pt",
        padding=True
    ).to(DEVICE)


    with torch.no_grad():
        outputs = model.get_text_features(**inputs)

        if hasattr(outputs, "text_embeds"):
            text_features = outputs.text_embeds
        elif hasattr(outputs, "pooler_output"):
            text_features = outputs.pooler_output
        else:
            text_features = outputs

    text_features = F.normalize(
        text_features,
        dim=-1
    )

    normal_features = text_features[:len(normal_prompts)].mean(
        dim=0,
        keepdim=True
    )

    defect_features = text_features[len(normal_prompts):].mean(
        dim=0,
        keepdim=True
    )

    normal_features = F.normalize(
        normal_features,
        dim=-1
    )

    defect_features = F.normalize(
        defect_features,
        dim=-1
    )

    return torch.cat(
        [
            normal_features,
            defect_features
        ],
        dim=0
    )


# ==========================
# Découpage de l'image
# ==========================

def extract_windows(image):
    """
    Découpe l'image en plusieurs zones
    pour analyser les défauts localisés.
    """

    width, height = image.size

    patches = []
    coordinates = []

    for y in range(0, height - WINDOW_SIZE[1] + 1, STRIDE):

        for x in range(0, width - WINDOW_SIZE[0] + 1, STRIDE):

            patch = image.crop(
                (
                    x,
                    y,
                    x + WINDOW_SIZE[0],
                    y + WINDOW_SIZE[1]
                )
            )

            patches.append(patch)
            coordinates.append((x, y))

    return patches, coordinates, (width, height)



# ==========================
# Prédiction WinCLIP
# ==========================

def predict_image(image, category="metal_nut"):
    """
    Analyse une image et retourne
    le diagnostic de conformité.
    """

    image = image.convert("RGB")

    text_features = encode_text(category)

    patches, coordinates, size = extract_windows(image)


    if not patches:
        patches = [
            image.resize(WINDOW_SIZE)
        ]

        coordinates = [
            (0, 0)
        ]

    scores = []

    with torch.no_grad():

        inputs = processor(
            images=patches,
            return_tensors="pt"
        ).to(DEVICE)

        outputs = model.get_image_features(
            **inputs
        )

        if hasattr(outputs, "image_embeds"):
            image_features = outputs.image_embeds
        elif hasattr(outputs, "pooler_output"):
            image_features = outputs.pooler_output
        else:
            image_features = outputs

        image_features = F.normalize(
            image_features,
            dim=-1
        )

        similarity = (
            100 *
            image_features @ text_features.T
        ).softmax(dim=-1)

        scores = similarity[:, 1].cpu().numpy()

    width, height = size

    heatmap = np.zeros(
        (
            height,
            width
        )
    )

    count_map = np.zeros(
        (
            height,
            width
        )
    )


    for score, (x, y) in zip(scores, coordinates):

        heatmap[
            y:y+WINDOW_SIZE[1],
            x:x+WINDOW_SIZE[0]
        ] += score


        count_map[
            y:y+WINDOW_SIZE[1],
            x:x+WINDOW_SIZE[0]
        ] += 1

    heatmap = np.divide(
        heatmap,
        count_map,
        out=np.zeros_like(heatmap),
        where=count_map != 0
    )

    heatmap = gaussian_filter(
        heatmap,
        sigma=4
    )

    anomaly_score = float(
        heatmap.max()
    )

    status = (
        "defaut"
        if anomaly_score > ANOMALY_THRESHOLD
        else "conforme"
    )

    return {
        "status": status,
        "confidence": round(anomaly_score, 1),
        "anomaly_score": round(anomaly_score, 1)
    }