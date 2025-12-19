import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Analyse Netflix", layout="wide")
st.title("Analyse du dataset Netflix")

CSV_PATH = "netflix_titles.csv"

# --- Lecture + sécurité ---
if not os.path.exists(CSV_PATH):
    st.error(f"Fichier introuvable: {CSV_PATH}. Vérifie qu’il est bien dans le repo GitHub.")
    st.stop()

try:
    df = pd.read_csv(CSV_PATH)
except pd.errors.EmptyDataError:
    st.error("Le fichier netflix_titles.csv est vide ou illisible.")
    st.stop()

# --- Nettoyage / features ---
df["date_added"] = pd.to_datetime(df.get("date_added"), errors="coerce")
df["year_added"] = df["date_added"].dt.year

cols_to_fill = ["director", "cast", "country"]
for c in cols_to_fill:
    if c in df.columns:
        df[c] = df[c].fillna("Unknown")

# =========================
# 1) Aperçu
# =========================
st.subheader("Aperçu du dataset")
c1, c2, c3 = st.columns(3)
c1.metric("Lignes", df.shape[0])
c2.metric("Colonnes", df.shape[1])
c3.metric("Duplicats", int(df.duplicated().sum()))

st.dataframe(df.head(20), use_container_width=True)

# =========================
# 2) Répartition Films / Séries
# =========================
st.subheader("Répartition Films / Séries")
type_counts = df["type"].value_counts()

fig, ax = plt.subplots()
ax.pie(type_counts, labels=type_counts.index, autopct="%1.1f%%", startangle=90)
ax.set_title("Répartition des contenus Netflix")
ax.axis("equal")
st.pyplot(fig)

# =========================
# 3) Contenus ajoutés par année
# =========================
st.subheader("Nombre de contenus ajoutés par année")
adds_per_year = df["year_added"].value_counts().sort_index()

fig, ax = plt.subplots()
ax.plot(adds_per_year.index, adds_per_year.values)
ax.set_title("Évolution des contenus ajoutés sur Netflix par année")
ax.set_xlabel("Année")
ax.set_ylabel("Nombre de contenus ajoutés")
ax.grid(True)
st.pyplot(fig)

# =========================
# 4) Films vs Séries ajoutés par année
# =========================
st.subheader("Évolution des films et séries ajoutés")
adds_by_year_type = (
    df.groupby(["year_added", "type"]).size().unstack(fill_value=0).sort_index()
)

fig, ax = plt.subplots()
for col in adds_by_year_type.columns:
    ax.plot(adds_by_year_type.index, adds_by_year_type[col], label=col)

ax.set_title("Films vs Séries ajoutés par année")
ax.set_xlabel("Année")
ax.set_ylabel("Nombre")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# =========================
# 5) Top 10 pays producteurs
# =========================
st.subheader("Top 10 des pays producteurs")
df_country = df.dropna(subset=["country"])
countries = df_country["country"].astype(str).str.split(", ").explode()
top_countries = countries.value_counts().head(10)

fig, ax = plt.subplots()
top_countries.plot(kind="bar", ax=ax)
ax.set_title("Top 10 des pays producteurs de contenus Netflix")
ax.set_xlabel("Pays")
ax.set_ylabel("Nombre de contenus")
ax.grid(True, axis="y")
st.pyplot(fig)

# =========================
# 6) Top 10 genres
# =========================
st.subheader("Top 10 des genres les plus présents")
df_genre = df.dropna(subset=["listed_in"])
genres = df_genre["listed_in"].astype(str).str.split(", ").explode()
top_genres = genres.value_counts().head(10)

fig, ax = plt.subplots()
top_genres.plot(kind="bar", ax=ax)
ax.set_title("Top 10 des genres les plus présents sur Netflix")
ax.set_xlabel("Genre")
ax.set_ylabel("Nombre de contenus")
ax.grid(True, axis="y")
st.pyplot(fig)
