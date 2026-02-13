from taxonomy import SPORT_OPTIONS
from config import COUNTRIES
'''
This module defines the questions
 to ask users and the options for each question.
'''
QUESTIONS = [
    {
        "id": "country",
        "text": "1) Which country are you shopping from?",
        "widget": "radio",
        "options": list(COUNTRIES.keys()),
    },
    {
        "id": "customer_id",
        "text": "2) Do you have a customer ID? If yes, enter it below (leave blank if not).",
        "widget": "text_input",
        "options": [],
    },
    {
        "id": "gender",
        "text": "3) Which product universe are you shopping today?",
        "widget": "radio",
        "options": ["Men", "Women"],
    },
    {
        "id": "sport",
        "text": "4) Which sport category are you looking for?",
        "widget": "selectbox",
        "options": SPORT_OPTIONS,
    },
    {
        "id": "product_type",
        "text": "5) What product type are you interested in?",
        "widget": "selectbox",
        "options": [],
    },
    {
        "id": "subtype",
        "text": "6) What are you specifically looking for?",
        "widget": "selectbox",
        "options": [],
    },
    {
        "id": "price_range",
        "text": "7) You are shopping for products in what price ranges?",
        "widget": "radio",
        "options": ["Budget(0-15)", "Mid-range(15-35)", "Premium(35-75)", "Luxury(75+)"],
    },
]