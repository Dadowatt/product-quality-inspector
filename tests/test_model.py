from PIL import Image
from app.model import predict_image


image = Image.open("test.png")

result = predict_image(image)

print(result)