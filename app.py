
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador de Stats Automáticas", layout="centered")
st.title("📦 Simulación de Carga Automática de Stats")

st.markdown("Esta demo simula la carga automática de estadísticas desde una API externa.")

# URL simulada (en tu app real sería una URL pública tipo GitHub Raw o un backend)
json_url = "https://raw.githubusercontent.com/tu_usuario/tu_repo/main/sample_stats.json"  # Reemplazar con link real

st.info("Este ejemplo usa un archivo JSON precargado que simula la respuesta de una API de estadísticas.")

uploaded = st.file_uploader("O subí tu archivo JSON con estadísticas", type=["json"])

if uploaded:
    df = pd.read_json(uploaded)
    st.success("✅ Archivo cargado exitosamente")
    st.dataframe(df)

    # Cálculo de dobles realizados
    df["Dobles Realizados"] = (df["Puntos"] - (df["Triples"] * 3) - df["Libres"]) / 2
    df["Dobles Intentados"] = df["FGA"] - df["Triples"]

    st.markdown("### 🎯 Análisis de Dobles")
    st.dataframe(df[["Puntos", "Triples", "Libres", "FGA", "Dobles Realizados", "Dobles Intentados"]])

    linea = st.number_input("Ingresá la línea para analizar dobles realizados:", step=0.5)
    aciertos = (df["Dobles Realizados"] > linea).sum()
    st.markdown(f"**Aciertos:** {aciertos} / {len(df)}")
else:
    st.warning("Subí un archivo JSON para continuar.")
