import streamlit as st
from PIL import Image
from pathlib import Path

from vision import detect_category, detect_food_name
from ai_recipe import generate_recipe

st.set_page_config(page_title="Desserts", layout="wide")

# Initialize session state
if "des_selected_image" not in st.session_state:
    st.session_state.des_selected_image = None
if "des_food_name" not in st.session_state:
    st.session_state.des_food_name = None
if "des_recipe" not in st.session_state:
    st.session_state.des_recipe = None

# Professional CSS Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem;
        background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2C3E50;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #a18cd1;
    }
    .sample-card {
        background: white;
        border-radius: 12px;
        padding: 0.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        margin-bottom: 1rem;
    }
    .sample-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .recipe-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 2rem;
        min-height: 400px;
    }
    .upload-section {
        background: #f8f9fa;
        border: 2px dashed #a18cd1;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-top: 1rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(161, 140, 209, 0.4);
    }
    .detected-food {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
    }
    .image-name {
        text-align: center;
        font-size: 0.85rem;
        color: #555;
        margin-top: 0.3rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🍰 Desserts Recipes</h1>', unsafe_allow_html=True)

IMG_DIR = Path("sample_images/desserts")

col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.markdown('<p class="section-header">📸 Sample Desserts</p>', unsafe_allow_html=True)
    
    images = list(IMG_DIR.glob("*"))
    img_cols = st.columns(3)
    
    for idx, img_path in enumerate(images):
        with img_cols[idx % 3]:
            img = Image.open(img_path)
            st.image(img, use_container_width=True)
            display_name = img_path.stem.replace("_", " ").title()
            st.markdown(f'<p class="image-name">{display_name}</p>', unsafe_allow_html=True)
            if st.button("Select", key=f"des_{img_path.name}"):
                st.session_state.des_selected_image = str(img_path)
                st.session_state.des_recipe = None
                st.rerun()
    
    st.markdown('<p class="section-header" style="margin-top: 2rem;">📤 Upload Your Own</p>', unsafe_allow_html=True)
    
    uploaded = st.file_uploader(
        "Choose a dessert image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
        key="des_uploader"
    )
    
    if uploaded:
        st.session_state.des_selected_image = uploaded
        st.session_state.des_recipe = None

with col_right:
    st.markdown('<p class="section-header">🍰 Generated Recipe</p>', unsafe_allow_html=True)
    
    if not st.session_state.des_selected_image:
        st.info("👈 Click on a sample image or upload your own to get started!")
    else:
        # Load the image
        if isinstance(st.session_state.des_selected_image, str):
            image = Image.open(st.session_state.des_selected_image).convert("RGB")
        else:
            image = Image.open(st.session_state.des_selected_image).convert("RGB")
        
        st.image(image, width=350)
        
        # Detect food name and category
        with st.spinner("🔍 Analyzing image..."):
            detected_category, confidence = detect_category(image)
            food_name = detect_food_name(image)
            st.session_state.des_food_name = food_name
        
        # Category validation
        expected_category = "dessert"
        is_correct_category = detected_category.lower() == expected_category
        
        if not is_correct_category:
            st.error(f"⚠️ This image appears to be a **{detected_category}**, not a dessert. Please upload a dessert image or go to the correct category page.")
            st.markdown(f'<div class="detected-food" style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);">🍽️ Detected: {food_name} ({detected_category})</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="detected-food">🍽️ Detected: {food_name}</div>', unsafe_allow_html=True)
            
            if st.button("✨ Generate Recipe", key="gen_recipe_des"):
                with st.spinner("👨‍🍳 Creating your recipe..."):
                    recipe = generate_recipe(
                        food_name=st.session_state.des_food_name,
                        category="dessert"
                    )
                    st.session_state.des_recipe = recipe
            
            if st.session_state.des_recipe:
                st.markdown("---")
                st.markdown(st.session_state.des_recipe)
