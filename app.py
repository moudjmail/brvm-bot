import streamlit as st
import pandas as pd
import os

st.title("📊 BRVM BOT PRO")

# Charger données
data = pd.read_csv("brvm_live.csv")

st.subheader("📋 Données BRVM")
st.dataframe(data)

# 🏆 TOP actions
st.subheader("🏆 TOP Actions")

if os.path.exists("top_actions.csv"):
    top_data = pd.read_csv("top_actions.csv")
    
    st.dataframe(top_data.head(5))

    # ✅ Affichage simple des noms
    st.subheader("🔥 Meilleures opportunités")
    for action in top_data["Action"].head(5):
        st.write(f"✅ {action}")

else:
    st.warning("⚠️ Lance d'abord le backtest (python backtest_global.py)")

# 📈 Graphique
st.subheader("📈 Graphique des prix")
st.line_chart(data["Prix"])