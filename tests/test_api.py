from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_inspect_image():

    with open("tests/test_images/piece_test.jpg", "rb") as image_file:

        response = client.post(
            "/inspect-image",
            files={
                "image": (
                    "piece_test.jpg",
                    image_file,
                    "image/jpeg"
                )
            },
            data={
                "category": "metal_nut"
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert "confidence" in data
    assert "anomaly_score" in data

    assert data["status"] in [
        "conforme",
        "defaut"
    ]