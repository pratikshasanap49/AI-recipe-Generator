import streamlit as st
import base64
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Recipe Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- BACKGROUND ----------------
def set_bg(image_path):
    img = Path(image_path).read_bytes()
    encoded = base64.b64encode(img).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
                url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}

        /* NAVBAR */
        .navbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 60px;
            font-size: 18px;
        }}

        .nav-links a {{
            margin-left: 30px;
            text-decoration: none;
            color: #eee;
            font-weight: 500;
        }}

        .nav-links a:hover {{
            color: #00ffd5;
        }}

        /* CARDS */
        .card {{
            background: linear-gradient(
                135deg,
                rgba(255,255,255,0.15),
                rgba(255,255,255,0.05)
            );
            backdrop-filter: blur(12px);
            padding: 45px 20px;
            border-radius: 22px;
            text-align: center;
            font-size: 26px;
            color: white;
            transition: 0.4s ease;
            cursor: pointer;
        }}

        .card:hover {{
            transform: scale(1.08);
            box-shadow: 0 0 30px rgba(0,255,213,0.6);
        }}

        /* MOBILE */
        @media (max-width: 900px) {{
            .navbar {{
                padding: 15px 20px;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("assets/home_bg.jpeg")

# ---------------- NAVBAR ----------------
st.markdown(
    """
    <div class="navbar">
        <div style="font-size:26px;">🍽️ AI Recipes</div>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/Beverages">Beverages</a>
            <a href="/Desserts">Desserts</a>
            <a href="/Main_Course">Main Course</a>
            <a href="/Snacks">Snacks</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- HERO ----------------
st.markdown("""
<br>
<h1 style='text-align:center; font-size:64px;'>
Discover Recipes from Images
</h1>
<p style='text-align:center; font-size:22px; color:#ccc;'>
AI-powered food recognition & recipe generation
</p>
<br><br>
""", unsafe_allow_html=True)

# ---------------- CATEGORY GRID ----------------
col1, col2, col3, col4 = st.columns(4)

def card(title, emoji, page):
    st.markdown(
        f"""
        <a href="/{page}" style="text-decoration:none;">
            <div class="card">
                <div style="font-size:55px;">{emoji}</div>
                <b>{title}</b>
            </div>
        </a>
        """,
        unsafe_allow_html=True
    )

with col1:
    card("Beverages", "🍹", "Beverages")

with col2:
    card("Desserts", "🍰", "Desserts")

with col3:
    card("Main Course", "🍽️", "Main_Course")

with col4:
    card("Snacks", "🍟", "Snacks")

# ---------------- FOOTER ----------------
st.markdown("""
<br><br>
<p style="text-align:center; color:#aaa;">
Powered by DeepSeek AI via OpenRouter • Built with Streamlit
</p>
""", unsafe_allow_html=True)
