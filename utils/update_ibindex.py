import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import requests
import json
API_URL = "https://ibindex.se/ibi//index/getProducts.req"

  # Exempel-URL — justera efter korrekt endpoint

def fetch_ibindex_discounts():
    resp = requests.get(API_URL)
    resp.raise_for_status()
    return resp.json()

def update_mock_data(output_file="ibindex_data.py"):
    data = fetch_ibindex_discounts()
    mock = {}

    for item in data:
        name = item.get("productName")
        discount = item.get("netAssetValueRebatePremium")
        if name and discount is not None:
            mock[name] = {
                "discount": round(discount, 2),
                "holdings": {}  # Behöver fyllas manuellt eller via annan data
            }

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("MOCK_DATA = ")
        json.dump(mock, f, indent=4, ensure_ascii=False)

    print(f"✅ Uppdaterade substansrabatter och sparade till `{output_file}`")

if __name__ == "__main__":
    update_mock_data()
