# 📊 Analyse du Marché High-Tech Tunisie 2026

Ce projet d'ingénierie en IA et Data Science automatise la collecte et l'analyse des prix des smartphones en Tunisie.

## 🛠️ Architecture du Projet
1. **Collecte (`scraper_tech.py`)** : Scraping multi-pages automatisé sur Tunisianet (BeautifulSoup/Requests).
2. **Traitement (`data_cleaning.py`)** : Nettoyage, extraction de la RAM par Regex et création d'un score de performance/prix exclusif.
3. **API (`main.py`)** : Exposition des statistiques du marché via FastAPI.
4. **Visualisation (`app.py`)** : Dashboard décisionnel interactif sous Streamlit avec analyses de distribution et recommandations intelligentes.

## 🚀 Installation
pip install -r requirements.txt
streamlit run app.py
