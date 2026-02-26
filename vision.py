import torch
from transformers import CLIPProcessor, CLIPModel
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"

# CLIP (category detection)
clip_model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
).to(device)

clip_processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

# BLIP (food name detection)
blip_processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(device)

CATEGORIES = {
    "beverage": ["a drink", "juice", "tea", "coffee", "smoothie", "milkshake", "soda", "lemonade"],
    "dessert": ["a dessert", "cake", "ice cream", "pastry", "cookies", "chocolate", "pudding", "donut"],
    "snack": ["a snack", "street food", "fried food", "pizza", "sandwich", "burger", "french fries", "samosa", "chips", "nachos", "hot dog"],
    "main course": ["a full meal", "rice dish", "curry", "pasta with meat", "roasted chicken", "steak", "biryani", "fish curry", "dal rice"]
}

def detect_category(image: Image.Image):
    texts = []
    mapping = []

    for cat, prompts in CATEGORIES.items():
        for p in prompts:
            texts.append(p)
            mapping.append(cat)

    inputs = clip_processor(
        text=texts,
        images=image,
        return_tensors="pt",
        padding=True
    ).to(device)

    with torch.no_grad():
        outputs = clip_model(**inputs)

    probs = outputs.logits_per_image.softmax(dim=1)[0]
    best = probs.argmax().item()

    return mapping[best], float(probs[best])

def detect_food_name(image: Image.Image):
    inputs = blip_processor(image, return_tensors="pt").to(device)

    with torch.no_grad():
        out = blip_model.generate(**inputs, max_new_tokens=20)

    caption = blip_processor.decode(out[0], skip_special_tokens=True)
    return caption
