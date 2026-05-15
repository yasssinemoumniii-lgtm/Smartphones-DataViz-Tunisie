import pandas as pd
import re

def clean_and_enhance_data(csv_file):
    # Chargement des données brutes
    df = pd.read_csv(csv_file)
    
    # 1. Nettoyage du Prix (Conversion en Float)
    df['prix'] = df['prix_brut'].str.replace(r'[^\d]', '', regex=True).astype(float) / 1000
    
    # 2. Extraction de la Marque (Premier mot en majuscules)
    df['marque'] = df['nom'].apply(lambda x: x.split()[0].upper())
    
    # 3. Extraction de la RAM (Recherche de Go ou GB)
    def extract_ram(text):
        match = re.search(r'(\d+)\s*(?:Go|GB|RAM)', text, re.IGNORECASE)
        return int(match.group(1)) if match else None

    df['ram_gb'] = df['nom'].apply(extract_ram)
    
    # 4. Diversification : Segmentation par Gamme
    df['gamme'] = pd.cut(df['prix'], bins=[0, 800, 1500, 5000], 
                         labels=['Économique', 'Standard', 'Premium'])
    
    # 5. Calcul du Score Performance/Prix
    # Plus le score est bas, meilleur est le rapport performance/prix
    df['score_prix_perf'] = df['prix'] / df['ram_gb']
    
    # Nettoyage final : suppression des lignes sans RAM détectée
    df_clean = df.dropna(subset=['ram_gb'])
    
    return df_clean

if __name__ == "__main__":
    # Test du nettoyage sur le fichier généré par le scraper
    try:
        df_final = clean_and_enhance_data('smartphones_bruts.csv')
        df_final.to_csv('smartphones_tunisie_2026.csv', index=False)
        print("Nettoyage et diversification terminés avec succès !")
    except Exception as e:
        print(f"Erreur lors du nettoyage : {e}")
