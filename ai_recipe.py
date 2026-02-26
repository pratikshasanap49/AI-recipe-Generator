# import base64
# import requests
#
# OPENROUTER_API_KEY = "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"
#
# def generate_recipe(image_bytes, expected_category):
#     """
#     image_bytes: bytes
#     expected_category: snack / dessert / beverage / main course
#     """
#
#     image_b64 = base64.b64encode(image_bytes).decode()
#
#     prompt = f"""
# You are a professional chef.
#
# 1. Identify the food in the image
# 2. Decide its category (snack, dessert, beverage, main course)
# 3. If the category is NOT "{expected_category}", respond exactly:
#    ERROR: This image is not a {expected_category}
#
# Otherwise provide:
# - Title
# - Category
# - Ingredients
# - Steps
# """
#
#     payload = {
#         "model": "openai/gpt-4o-mini",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": prompt},
#                     {
#                         "type": "image_url",
#                         "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
#                     }
#                 ]
#             }
#         ]
#     }
#
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json"
#     }
#
#     response = requests.post(
#         "https://openrouter.ai/api/v1/chat/completions",
#         json=payload,
#         headers=headers,
#         timeout=60
#     )
#
#     data = response.json()
#
#     if "choices" not in data:
#         return "ERROR: Failed to analyze image"
#
#     text = data["choices"][0]["message"]["content"]
#
#     return text



#
# import base64
# import requests
# import os
#
# OPENROUTER_API_KEY = os.getenv("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")
#
# VISION_MODEL = "tngtech/deepseek-r1t2-chimera:free"
#
# def generate_recipe(image_bytes: bytes, expected_category: str) -> str:
#     try:
#         # Convert image to base64
#         image_b64 = base64.b64encode(image_bytes).decode("utf-8")
#
#         prompt = f"""
# You are a professional chef AI.
#
# Analyze the food image and generate a detailed recipe.
#
# Category must be: {expected_category}
#
# Respond ONLY in this format:
#
# Title:
# Category:
# Ingredients:
# - item
# Steps:
# 1. step
# """
#
#         payload = {
#             "model": VISION_MODEL,
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": prompt},
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": f"data:image/jpeg;base64,{image_b64}"
#                             },
#                         },
#                     ],
#                 }
#             ],
#             "max_tokens": 700,
#         }
#
#         headers = {
#             "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#             "Content-Type": "application/json",
#         }
#
#         response = requests.post(
#             "https://openrouter.ai/api/v1/chat/completions",
#             headers=headers,
#             json=payload,
#             timeout=60,
#         )
#
#         if response.status_code != 200:
#             return f"ERROR: API failed ({response.status_code})\n{response.text}"
#
#         data = response.json()
#
#         return data["choices"][0]["message"]["content"]
#
#     except Exception as e:
#         return f"ERROR: {str(e)}"


#
# import requests
# import os
#
# OPENROUTER_API_KEY = os.getenv("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")
#
# def generate_recipe(food_name, category):
#     prompt = f"""
# You are a professional chef.
#
# Create a detailed {category} recipe for:
# Food name: {food_name}
#
# Include:
# - Title
# - Ingredients
# - Step-by-step instructions
# - Tips
# """
#
#     response = requests.post(
#         "https://openrouter.ai/api/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#             "Content-Type": "application/json"
#         },
#         json={
#             "model": "tngtech/deepseek-r1t2-chimera:free",
#             "messages": [
#                 {"role": "user", "content": prompt}
#             ],
#             "temperature": 0.7,
#             "max_tokens": 600
#         },
#         timeout=60   # 🔥 IMPORTANT
#     )
#
#     response.raise_for_status()
#     return response.json()["choices"][0]["message"]["content"]

import requests
import os
import time
from dotenv import load_dotenv

load_dotenv(override=True)

# Free Groq API - get your key at https://console.groq.com/keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_recipe(food_name, category, max_retries=3):
    prompt = f"""
You are a professional chef.

Create a detailed {category} recipe for:
Food: {food_name}

Include:
- Title
- Ingredients
- Step-by-step instructions
- Tips
"""

    for attempt in range(max_retries):
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 600
            },
            timeout=60
        )

        if response.status_code == 429:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                time.sleep(wait_time)
                continue
            else:
                raise Exception("Rate limit exceeded. Please wait a minute and try again.")
        
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
