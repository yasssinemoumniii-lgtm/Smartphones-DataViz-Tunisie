from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Chargement des données scrapées et nettoyées
df = pd.read_csv('smartphones_tunisie_2026.csv')

@app.get("/")
def home():
    return {"message": "API du Marché High-Tech Tunisie 2026", "status": "Online"}

@app.get("/produits")
def get_all_products():
    """Retourne la liste complète des smartphones scrapés"""
    return df.to_dict(orient="records")

@app.get("/stats")
def get_market_stats():
    """Retourne des indicateurs décisionnels pour le prof"""
    return {
        "prix_moyen": round(df['prix'].mean(), 2),
        "total_modeles": len(df),
        "marques_plus_presentes": df['marque'].value_counts().head(3).to_dict()
    }
