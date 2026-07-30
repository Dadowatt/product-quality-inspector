from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from PIL import Image
from io import BytesIO

from app.model import predict_image
from app.schemas import InspectionResponse

# ==========================
# Configuration
# ==========================

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 Mo


# ==========================
# Création de l'API
# ==========================

app = FastAPI(
    title="Vision Quality API",
    description="API de contrôle qualité par détection d'anomalies",
    version="1.0"
)


# ==========================
# Endpoint inspection image
# ==========================

@app.post(
    "/inspect-image",
    response_model=InspectionResponse
)
async def inspect_image(
    image: UploadFile = File(...),
    category: str = Form("metal_nut")
):

    # ==========================
    # Validation du fichier image
    # ==========================

    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Le fichier envoyé n'est pas une image"
        )

    # ==========================
    # Vérification de la taille
    # ==========================

    image_bytes = await image.read()

    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image trop volumineuse (maximum 5 Mo)"
        )
    

    # ==========================
    # Lecture et validation de l'image
    # ==========================

    try:
        pil_image = Image.open(
            BytesIO(image_bytes)
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Image invalide ou corrompue"
        )


    # ==========================
    # Analyse IA
    # ==========================

    try:
        result = predict_image(
            pil_image,
            category=category
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur pendant l'analyse du modèle : {str(e)}"
        )

    return result

# ==========================
# Route de test
# ==========================

@app.get("/")
def root():
    return {
        "message": "Vision Quality API opérationnelle"
    }