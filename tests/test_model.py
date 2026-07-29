from PIL import Image

from app.model import predict_image


def test_predict_image():
    """
    Vérifie que le modèle retourne
    un diagnostic valide.
    """

    # ==========================
    # Chargement de l'image test
    # ==========================

    image = Image.open(
        "tests/test_images/piece_test.jpg"
    ).convert("RGB")

    # ==========================
    # Analyse de l'image
    # ==========================

    result = predict_image(
        image=image,
        category="metal_nut"
    )

    # ==========================
    # Vérification du résultat
    # ==========================

    assert result["status"] in [
        "conforme",
        "defaut"
    ]

    assert 0 <= result["confidence"] <= 1

    assert 0 <= result["anomaly_score"] <= 1