import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# För att kunna använda custom JS-villkor
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support.expected_conditions import _find_elements

# Ladda MOCK_DATA
with open("ibindex_data.py", encoding="utf-8") as f:
    content = f.read().replace("MOCK_DATA = ", "")
    MOCK_DATA = json.loads(content)

# Setup headless browser
opts = Options()
opts.add_argument("--headless")
opts.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=opts)

# Gå till BURE
driver.get("https://ibindex.se/ibi/#/company/BURE")

# Vänta max 10 sek tills window.ibiApp.holdings finns
WebDriverWait(driver, 10).until(
    lambda d: d.execute_script("return !!(window.ibiApp && window.ibiApp.holdings && window.ibiApp.holdings.data)")
)

# Nu när datan är laddad – hämta holdings
holdings = driver.execute_script("return window.ibiApp.holdings.data")

# Skriv till MOCK_DATA
if "Bure Equity" in MOCK_DATA:
    MOCK_DATA["Bure Equity"]["holdings"] = {
        h["holdingName"]: h["holdingValue"] for h in holdings
    }
    print(f"✅ {len(holdings)} innehav hämtade för Bure Equity")
else:
    print("❌ Bure Equity finns inte i MOCK_DATA")

driver.quit()

# Spara uppdaterad data
with open("ibindex_data.py", "w", encoding="utf-8") as f:
    f.write("MOCK_DATA = ")
    json.dump(MOCK_DATA, f, indent=4, ensure_ascii=False)

