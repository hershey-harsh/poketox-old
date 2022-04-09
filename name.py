from transformers import ViTForImageClassification, ViTFeatureExtractor
from PIL import Image
import torch

# Loading in Model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = ViTForImageClassification.from_pretrained( "pokemon_classifier").to(device)
feature_extractor = ViTFeatureExtractor.from_pretrained('pokemon_classifier')

# Caling the model on a test image
def solve(url):
  response = requests.get(url)
  file = open("pokemon.png", "wb")
  file.write(response.content)
  file.close()
  img = Image.open('pokemon.png')
  extracted = feature_extractor(images=img, return_tensors='pt').to(device)
  predicted_id = model(**extracted).logits.argmax(-1).item()
  predicted_pokemon = model.config.id2label[predicted_id]
  return predicted_pokemon
