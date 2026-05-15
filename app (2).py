import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Stratégie Marché Tech 2026", layout="wide")

# Chargement des données
df = pd.read_csv('smartphones_tunisie_2026.csv')

# --- SIDEBAR (Filtres Décisionnels) ---
st.sidebar.header("🎯 Aide à la décision")
selected_marques = st.sidebar.multiselect("Marques cibles", df['marque'].unique(), default=df['marque'].unique())
budget = st.sidebar.slider("Votre budget (DT)", int(df['prix'].min()), int(df['prix'].max()), (0, 2500))

df_filtered = df[(df['marque'].isin(selected_marques)) & (df['prix'].between(budget[0], budget[1]))]

# --- HEADER ---
st.title("🚀 Dashboard Décisionnel : Smartphones Tunisie")
st.markdown(f"Analyse basée sur **{len(df)}** produits scrapés en temps réel.")

# --- KPIs ---
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Modèles Filtrés", len(df_filtered))
kpi2.metric("Prix Moyen", f"{df_filtered['prix'].mean():.0f} DT")
kpi3.metric("Meilleur Score Perf/Prix", f"{df_filtered['score_prix_perf'].min():.2f}")
kpi4.metric("Marque Dominante", df_filtered['marque'].value_counts().idxmax())

st.divider()

# --- ANALYSE GRAPHIQUE ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Segmentation par Gamme")
    fig_sun = px.sunburst(df_filtered, path=['gamme', 'marque'], values='prix',
                          title="Répartition de la valeur par segment")
    st.plotly_chart(fig_sun, use_container_width=True)

with col2:
    st.subheader("💡 Où sont les meilleures opportunités ?")
    # Scatter plot décisionnel : RAM vs PRIX avec taille selon le ratio
    fig_scatter = px.scatter(df_filtered, x="ram_gb", y="prix", color="marque",
                             size=1/df_filtered['score_prix_perf'], # Plus le score est petit, plus la bulle est grosse
                             hover_name="nom", title="Plus la bulle est grosse, meilleur est le rapport Performance/Prix")
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- ANALYSE DE DISTRIBUTION ---
st.subheader("📉 Distribution des prix par Marque")
fig_box = px.box(df_filtered, x="marque", y="prix", color="marque", points="all",
                 title="Étendue des tarifs par constructeur")
st.plotly_chart(fig_box, use_container_width=True)

# --- RECOMMANDATION AUTOMATISÉE ---
st.subheader("✅ Recommandation de l'IA")
best_deal = df_filtered.sort_values('score_prix_perf').iloc[0]
st.success(f"D'après les données, le meilleur choix dans votre budget est le **{best_deal['nom']}** ({best_deal['prix']} DT) avec un excellent score de performance.")

# Affichage des données brutes
with st.expander("Consulter la base de données complète"):
    st.dataframe(df_filtered.sort_values('score_prix_perf'))
