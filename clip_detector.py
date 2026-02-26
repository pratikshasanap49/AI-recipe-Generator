# clip_detector.py
import torch
import clip
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

CATEGORY_LABELS = {
    "beverage": ["a photo of coffee", "a photo of tea", "a photo of juice"],
    "dessert": ["a photo of cake", "a photo of ice cream", "a photo of dessert"],
    "snack": ["a photo of burger", "a photo of fries", "a photo of samosa"],
    "main course": ["a photo of biryani", "a photo of rice", "a photo of pasta"]
}

def detect_food(image_path: str, category: str):
    image = preprocess(
        Image.open(image_path).convert("RGB")
    ).unsqueeze(0).to(device)

    labels = CATEGORY_LABELS[category]
    text = clip.tokenize(labels).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)

        # Normalize (VERY IMPORTANT)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        similarity = (image_features @ text_features.T).softmax(dim=-1)

    best_idx = similarity.argmax().item()
    confidence = similarity[0][best_idx].item()

    return {
        "match": confidence > 0.30,
        "label": labels[best_idx],
        "confidence": confidence
    }
