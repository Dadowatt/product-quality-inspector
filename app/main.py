from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from PIL import Image
from io import BytesIO

from app.model import predict_image
from app.schemas import InspectionResponse


app = FastAPI()


# ==========================
# Configuration sécurité
# ==========================

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

ALLOWED_TYPES = [
    "image/jpeg",
    "image/png"
]


# ==========================
# Route principale
# ==========================

@app.get("/")
def home():

    return {
        "message": "API contrôle qualité opérationnelle"
    }


# ==========================
# Inspection image
# ==========================

@app.post(
    "/inspect-image",
    response_model=InspectionResponse
)
async def inspect_image(
    file: UploadFile = File(...)
):

    # Vérification du format MIME

    if file.content_type not in ALLOWED_TYPES:

        raise HTTPException(
            status_code=400,
            detail="Format image non supporté. Utilisez PNG ou JPEG."
        )


    # Lecture du fichier en mémoire

    contents = await file.read()


    # Vérification de la taille

    if len(contents) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=413,
            detail="Image trop volumineuse (maximum 5 MB)."
        )


    try:

        image = Image.open(
            BytesIO(contents)
        )


        result = predict_image(image)


        return {

            "status": "conforme",

            "confidence": result["confidence"],

            "detected_object": result["label"]

        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Erreur traitement image : {str(e)}"
        )