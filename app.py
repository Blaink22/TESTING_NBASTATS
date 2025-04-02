# Streamlit app con opción manual o automática para cargar estadísticas NBA
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Análisis NBA", layout="centered")
st.title("🏀 Analizador de Dobles (Manual / Automático)")

# Selección de modo
modo = st.radio("Seleccioná cómo querés cargar los datos:", ["Carga manual", "Carga automática"])

num_partidos = 10

if modo == "Carga manual":
    st.markdown("Ingresa los datos de los **últimos 10 partidos** del jugador:")

    partidos_df = pd.DataFrame({
        "Puntos": [None]*num_partidos,
        "Triples": [None]*num_partidos,
        "Libres": [None]*num_partidos
    })

    data_input = st.data_editor(partidos_df, num_rows="fixed", use_container_width=True, key="partidos_m")

    if data_input.dropna().shape[0] < num_partidos:
        st.info("⬆️ Completa los 10 partidos para continuar.")
        st.stop()

elif modo == "Carga automática":
    st.markdown("Seleccioná un jugador de la NBA para cargar sus últimos 10 partidos:")
    jugador = st.text_input("Nombre del jugador", placeholder="Ej: LeBron James")

    if jugador:
        # Buscar jugador por nombre
        search_url = f"https://www.balldontlie.io/api/v1/players?search={jugador}"
        res = requests.get(search_url)
        players = res.json()["data"]

        if len(players) == 0:
            st.error("❌ No se encontró ningún jugador con ese nombre.")
            st.stop()

        player = players[0]  # Tomamos el primero como mejor coincidencia
        player_id = player["id"]
        st.success(f"Jugador encontrado: {player['first_name']} {player['last_name']}")

        # Obtener últimos partidos con stats
        stats_url = f"https://www.balldontlie.io/api/v1/stats?player_ids[]={player_id}&per_page=10"
        stats_res = requests.get(stats_url)
        stats_data = stats_res.json()["data"]

        if len(stats_data) == 0:
            st.warning("Este jugador no tiene partidos recientes cargados.")
            st.stop()

        data_input = pd.DataFrame([{ 
            "Puntos": s["pts"], 
            "Triples": s["fg3m"], 
            "Libres": s["ftm"] 
        } for s in stats_data])

        st.markdown("### 📊 Datos automáticos cargados")
        st.dataframe(data_input, use_container_width=True)

# Si tenemos datos cargados, calculamos DOBLES y análisis
if 'data_input' in locals():
    data_input["Dobles"] = (data_input["Puntos"] - (data_input["Triples"] * 3) - data_input["Libres"]) / 2
    st.markdown("### 📈 Dobles Calculados")
    st.dataframe(data_input, use_container_width=True)

    linea = st.number_input("🔹 Ingresá la línea a evaluar (dobles)", min_value=0.0, step=0.5)
    aciertos = (data_input["Dobles"] > linea).sum()
    st.markdown(f"### ✅ Aciertos: **{aciertos} / {num_partidos}**")

    if aciertos < 4:
        st.error("❌ Bajo rendimiento (menos de 4 aciertos)")
    elif 4 <= aciertos <= 6:
        st.warning("🔹 Rendimiento medio (entre 4 y 6 aciertos)")
    else:
        st.success("🌟 Buen rendimiento (7 o más aciertos)")
