import pandas as pd
import streamlit as st

from config import UI_ONLY_MODE, STOCK_CSV_PATH, COUNTRY_TO_CSV

def mock_stock_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Universe": ["Men", "Men", "Women"],
            "StoreCountry": ["FRA", "FRA", "GBR"],
            "Category": ["Badminton", "Basketball", "Football"],
            "ProductType": ["Equipment", "Equipment", "Shoes"],
            "FamilyLevel1": ["Racket", "Ball", "Shoes"],
            "FamilyLevel2": ["Mock Racket A", "Mock Ball B", "Mock Shoes C"],
            "Quantity": [5, 0, 12],
            "median_price": [19.99, 12.50, 45.00],
        }
    )

def mock_catalog_df() -> pd.DataFrame:
    return pd.DataFrame({"ClientID": ["123", "ABC999", "00042"]})

@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def get_stock_df() -> pd.DataFrame:
    if UI_ONLY_MODE:
        return mock_stock_df()
    return load_csv(str(STOCK_CSV_PATH))

def get_catalog_df_for_country(country_code: str) -> pd.DataFrame:
    if UI_ONLY_MODE:
        return mock_catalog_df()
    path = COUNTRY_TO_CSV.get(country_code)
    if not path:
        raise ValueError(f"No catalog CSV mapped for country: {country_code}")
    return load_csv(str(path))
