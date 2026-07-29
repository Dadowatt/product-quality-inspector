import os

from dotenv import load_dotenv
import torch
import timm

from PIL import Image

from timm.data import resolve_model_data_config
from timm.data.transforms_factory import create_transform

from torchvision.models import MobileNet_V3_Small_Weights

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# ==========================
# Configuration du modèle
# ==========================

MODEL_NAME = "mobilenetv3_small_100.lamb_in1k"
MODEL_REVISION = "1824797e7887cbec1990e4adbd6675960a36c589"


# ==========================
# Device
# ==========================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ==========================
# Chargement du modèle
# ==========================

if HF_TOKEN:
    os.environ["HF_TOKEN"] = HF_TOKEN
    
model = timm.create_model(
    MODEL_NAME,
    pretrained=True
)

model.to(DEVICE)
model.eval()


# ==========================
# Préparation des images
# ==========================

data_config = resolve_model_data_config(model)

transform = create_transform(
    **data_config,
    is_training=False
)


# ==========================
# Labels ImageNet
# ==========================

categories = MobileNet_V3_Small_Weights.DEFAULT.meta["categories"]


# ==========================
# Prediction
# ==========================

def predict_image(image: Image.Image):

    # Assurer un format RGB
    image = image.convert("RGB")

    tensor = transform(image)

    tensor = tensor.unsqueeze(0)

    tensor = tensor.to(DEVICE)


    with torch.no_grad():

        output = model(tensor)

        probabilities = torch.nn.functional.softmax(
            output[0],
            dim=0
        )


    confidence, index = torch.max(
        probabilities,
        dim=0
    )


    label = categories[index.item()]


    return {
        "label": label,
        "confidence": round(
            float(confidence),
            3
        )
    }