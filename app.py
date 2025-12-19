import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Analyse du dataset Netflix")

df = pd.read_csv("netflix_titles.csv")

st.subheader("Aperçu du dataset")
st.dataframe(df.head())

st.subheader("Répartition Films / Séries")
type_counts = df["type"].value_counts()

fig, ax = plt.subplots()
ax.pie(type_counts, labels=type_counts.index, autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.pyplot(fig)
