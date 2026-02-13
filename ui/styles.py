import streamlit as st
from config import BASE_DIR
from utils import get_base64_image
'''
This module contains the global CSS styles for the Streamlit app, including:
- Hiding default Streamlit UI elements (header, toolbar, etc.) for a cleaner look.
- Setting a custom background image for the app.
- Styling the main content container with a semi-transparent background and rounded corners.
- Positioning a logo image at the top-right corner of the app.
- Customizing font sizes for questions, buttons, and dataframes for better readability.
'''
def inject_global_css():
    bg_path = BASE_DIR / "pictures" / "background.jpg"
    logo_path = BASE_DIR / "pictures" / "logo.png"

    bg_base64 = get_base64_image(bg_path)
    logo_base64 = get_base64_image(logo_path)

    st.markdown(
        f"""
        <style>
        header[data-testid="stHeader"] {{
            display: none;
        }}

        div[data-testid="stDecoration"] {{
            display: none;
        }}

        div[data-testid="stToolbar"] {{
            display: none;
        }}

        div[data-testid="stAppViewContainer"] {{
            padding-top: 0rem !important;
        }}

        .stApp {{
            background-image: url("data:image/jpg;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        .block-container {{
            background-color: rgba(255, 255, 255, 0.88);
            padding: 2.5rem 2rem 2rem 2rem;
            border-radius: 16px;
            max-width: 900px;
            margin: 12vh auto 0 auto;
            position: relative;
        }}

        .app-logo {{
            position: absolute;
            top: -40px;
            right: 24px;
            z-index: 10;
            pointer-events: none;
        }}

        .app-logo img {{
            height: 120px;
            width: auto;
            display: block;
            background: transparent !important;
        }}

        h1 {{
            padding-right: 160px;
        }}

        .big-question {{
            font-size: 30px;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 0.8rem;
        }}

        button {{
            font-size: 16px !important;
            padding: 0.55em 1.2em !important;
        }}

        div[data-testid="stDataFrame"] {{
            font-size: 16px !important;
        }}
        </style>

        <div class="app-logo">
            <img src="data:image/png;base64,{logo_base64}" alt="Logo" />
        </div>
        """,
        unsafe_allow_html=True,
    )
