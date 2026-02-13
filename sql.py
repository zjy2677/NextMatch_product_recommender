import duckdb
import pandas as pd
from config import PRICE_BOUNDS
'''
This module contains the core logic to query the stock data based on user answers. 
'''
def query_stock(stock_df: pd.DataFrame, answers: dict) -> pd.DataFrame:
    # NOTE: price_range is intentionally ignored

    sql = """
    SELECT
        FamilyLevel2 AS product,
        CASE
            WHEN SUM(Quantity) > 0 THEN 'Available'
            ELSE 'Out of Stock'
        END AS status,
    FROM stock
    WHERE Universe = ?
      AND StoreCountry = ?
      AND Category = ?
      AND ProductType = ?
      AND FamilyLevel1 = ?
    GROUP BY FamilyLevel2
    LIMIT 5
    """

    params = [
        answers["gender"],
        answers["country"],
        answers["sport"],
        answers["product_type"],
        answers["subtype"],
    ]

    con = duckdb.connect(database=":memory:")
    con.register("stock", stock_df)
    df_out = con.execute(sql, params).fetchdf()
    return df_out
