from pathlib import Path

UI_ONLY_MODE = False
DEBUG_MODE = False

BASE_DIR = Path(__file__).resolve().parent

STOCK_CSV_PATH = BASE_DIR / "data" / "products_stores_stocks.csv"

COUNTRY_TO_CSV = {
    "USA": BASE_DIR / "data" / "catalog_USA.csv",
    "FRA": BASE_DIR / "data" / "catalog_FRA.csv",
    "GBR": BASE_DIR / "data" / "catalog_GBR.csv",
    "AUS": BASE_DIR / "data" / "catalog_AUS.csv",
    "DEU": BASE_DIR / "data" / "catalog_DEU.csv",
    "ARE": BASE_DIR / "data" / "catalog_ARE.csv",
    "BRA": BASE_DIR / "data" / "catalog_BRA.csv",
}

COUNTRIES = {
    "🇺🇸 United States of America": "USA",
    "🇫🇷 Republic of France": "FRA",
    "🇬🇧 United Kingdom": "GBR",
    "🇦🇺 Australia": "AUS",
    "🇩🇪 Federal Republic of Germany": "DEU",
    "🇦🇪 United Arab Emirates": "ARE",
    "🇧🇷 Brazil": "BRA",
}

PRICE_BOUNDS = {
    "Budget(0-15)": (0.0, 15.0),
    "Mid-range(15-35)": (15.0, 35.0),
    "Premium(35-75)": (35.0, 75.0),
    "Luxury(75+)": (75.0, None),
}
