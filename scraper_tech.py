import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_tunisianet_multipage(max_pages=5):
    all_products = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    for page in range(1, max_pages + 1):
        url = f"https://www.tunisianet.com.tn/301-smartphone-tunisie?page={page}"
        print(f"Extraction de la page {page}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200: break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            items = soup.find_all('article', class_='product-miniature')

            for item in items:
                try:
                    name = item.find('h2', class_='h3 product-title').text.strip()
                    price = item.find('span', class_='price').text.strip()
                    desc = item.find('div', class_='product-description').text.strip()
                    all_products.append({"nom": name, "prix_brut": price, "description": desc})
                except:
                    continue
            time.sleep(1) 
        except Exception as e:
            print(f"Erreur sur la page {page}: {e}")
            break
        
    return pd.DataFrame(all_products)

if __name__ == "__main__":
    df_raw = scrape_tunisianet_multipage(5)
    print(f"Extraction terminée : {len(df_raw)} produits récupérés.")
    df_raw.to_csv('smartphones_bruts.csv', index=False)
