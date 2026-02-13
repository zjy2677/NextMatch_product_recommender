## Installation

```bash
pip install -r requirements.txt
```
## Data files

The full dataset (`products_stores_stocks_with_prices.csv`, ~160 MB) is not included in this repository.
The dataset only contains a samle data from France market and only contains limited amount of pictures only 
as a demonstration
To run the app with real data:
1. Obtain the dataset separately
2. Place it in the `data/` folder
3. Update `STOCK_CSV_PATH` in `config.py` if needed

A small sample dataset is provided for demo and testing.

## How to use

Note that for country, you can only select France because data for other country is not provided so it will return 
no product recommendations. For France, you have two routes for testing:

1.Testing for prospects (non-registered customer):
France -> Skip ID -> Men -> Football -> Apparel -> Jersey
You will then see the recommendatiosn with pictures and a section where you could fill in your email and register!

2.Tesing for registered-customer:
France -> Use this ID: 2509961925537769 -> Badminton -> Equipement -> Racket
You will then see the recommendations with pictures plus a section "You may also like"

You could then test freely in France, but most of the products will not be shown with a pciture.
