import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.brvm.org/fr/cours-actions/0"
response = requests.get(url, verify=False)

soup = BeautifulSoup(response.text, "html.parser")

data = []
rows = soup.find_all("tr")

for row in rows:
    cols = row.find_all("td")
    
    # Vérifier qu'il y a assez de colonnes
    if len(cols) >= 4:
        action = cols[0].text.strip()
        prix = cols[3].text.strip().replace(" ", "")
        
        # Vérifier que le prix est un nombre
        if prix.replace(".", "").isdigit():
            data.append([action, prix])

df = pd.DataFrame(data, columns=["Action", "Prix"])
df.to_csv("brvm_live.csv", index=False)

print("✅ Données récupérées")