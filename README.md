# AI Recipe Generator

An AI-powered recipe generator that identifies food from images and creates detailed recipes using machine learning.

## Features

- **Image Recognition**: Upload food images and get them automatically identified
- **Category Detection**: Automatically classifies food into Beverages, Snacks, Desserts, or Main Course
- **AI Recipe Generation**: Generates detailed recipes with ingredients and step-by-step instructions
- **Category Validation**: Ensures uploaded images match the selected food category
- **Professional UI**: Modern, responsive interface with gradient styling

## Tech Stack

- **Frontend**: Streamlit
- **Image Recognition**: CLIP (OpenAI) for category detection
- **Image Captioning**: BLIP (Salesforce) for food name detection
- **Recipe Generation**: Groq API (LLaMA 3.1)
- **Language**: Python 3.11+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/AI_Recipe_project.git
cd AI_Recipe_project
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key from [Groq Console](https://console.groq.com/keys)

5. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
AI_Recipe_project/
├── app.py                 # Main application entry point
├── ai_recipe.py           # Recipe generation using Groq API
├── vision.py              # Image recognition (CLIP + BLIP)
├── pages/
│   ├── Beverages.py       # Beverages recipe page
│   ├── Snacks.py          # Snacks recipe page
│   ├── Desserts.py        # Desserts recipe page
│   └── Main_Course.py     # Main course recipe page
├── sample_images/         # Sample food images
│   ├── beverages/
│   ├── snacks/
│   ├── desserts/
│   └── main_course/
└── assets/                # Static assets
```

## Usage

1. Navigate to any category page (Beverages, Snacks, Desserts, Main Course)
2. Select a sample image or upload your own
3. The AI will detect the food and verify the category
4. Click "Generate Recipe" to get a detailed recipe

## License

MIT License
