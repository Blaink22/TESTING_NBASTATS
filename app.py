
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NBA Stats Analyzer", layout="centered")
st.title("🏀 NBA Stats Analyzer")

tabs = st.tabs(["Dobles Realizados", "Dobles Intentados", "Estadísticas Completas"])
num_partidos = 10

# ---------- TAB 1: Dobles Realizados ----------
with tabs[0]:
    st.subheader("🎯 Dobles Realizados")
    modo = st.radio("Seleccioná cómo cargar los datos:", ["Carga manual", "Carga automática"], key="modo_dobles")

    if modo == "Carga manual":
        df_manual = pd.DataFrame({
            "Puntos": [None]*num_partidos,
            "Triples": [None]*num_partidos,
            "Libres": [None]*num_partidos
        })
        data_input = st.data_editor(df_manual, num_rows="fixed", use_container_width=True, key="manual_realizados")

    else:
        jugador = st.text_input("Nombre del jugador (NBA)", placeholder="Ej: LeBron James")
        data_input = pd.DataFrame()
        if jugador:
            search_url = f"https://www.balldontlie.io/api/v1/players?search={jugador}"
            try:
                res = requests.get(search_url)
                if res.status_code != 200:
                    st.error("❌ Error al conectarse con la API.")
                    st.stop()
                players = res.json().get("data", [])
            except Exception:
                st.error("❌ No se pudo procesar la respuesta de la API.")
                st.stop()

            if not players:
                st.warning("No se encontró ningún jugador con ese nombre.")
                st.stop()

            player = players[0]
            st.success(f"Jugador encontrado: {player['first_name']} {player['last_name']}")
            stats_url = f"https://www.balldontlie.io/api/v1/stats?player_ids[]={player['id']}&per_page={num_partidos}"
            stats_res = requests.get(stats_url)
            stats_data = stats_res.json().get("data", [])

            if not stats_data:
                st.warning("Este jugador no tiene partidos recientes cargados.")
                st.stop()

            data_input = pd.DataFrame([{ 
                "Puntos": s["pts"], 
                "Triples": s["fg3m"], 
                "Libres": s["ftm"] 
            } for s in stats_data])
            st.dataframe(data_input, use_container_width=True)

    if not data_input.empty:
        cols = ["Puntos", "Triples", "Libres"]
        data_input[cols] = data_input[cols].apply(pd.to_numeric, errors="coerce").fillna(0)
        data_input["Dobles"] = (data_input["Puntos"] - (data_input["Triples"] * 3) - data_input["Libres"]) / 2
        st.markdown("### ✅ Dobles Calculados")
        st.dataframe(data_input, use_container_width=True)

        linea = st.number_input("Ingresá la línea a evaluar (dobles realizados)", min_value=0.0, step=0.5, key="linea_realizados")
        aciertos = (data_input["Dobles"] > linea).sum()
        st.markdown(f"**Aciertos sobre la línea:** {aciertos} / {len(data_input)}")

# ---------- TAB 2: Dobles Intentados ----------
with tabs[1]:
    st.subheader("🏹 Dobles Intentados")
    df_intentados = pd.DataFrame({
        "FGA (Tiros de campo intentados)": [None]*num_partidos,
        "Triples intentados": [None]*num_partidos
    })
    data_input2 = st.data_editor(df_intentados, num_rows="fixed", use_container_width=True, key="intentados")

    if data_input2.dropna().shape[0] == num_partidos:
        cols = data_input2.columns
        data_input2[cols] = data_input2[cols].apply(pd.to_numeric, errors="coerce").fillna(0)
        data_input2["Dobles Intentados"] = data_input2[cols[0]] - data_input2[cols[1]]
        st.markdown("### 🎯 Dobles Intentados Calculados")
        st.dataframe(data_input2, use_container_width=True)

        linea = st.number_input("Ingresá la línea a evaluar (dobles intentados)", min_value=0.0, step=0.5, key="linea_intentados")
        aciertos = (data_input2["Dobles Intentados"] > linea).sum()
        st.markdown(f"**Aciertos sobre la línea:** {aciertos} / {len(data_input2)}")

# ---------- TAB 3: Estadísticas Completas ----------
with tabs[2]:
    st.subheader("📊 Estadísticas Completas (Carga manual)")
    df_full = pd.DataFrame({
        "Puntos": [None]*num_partidos,
        "Triples": [None]*num_partidos,
        "Libres": [None]*num_partidos,
        "FGA": [None]*num_partidos,
        "3PT INT": [None]*num_partidos
    })
    full_input = st.data_editor(df_full, num_rows="fixed", use_container_width=True, key="full")

    if full_input.dropna().shape[0] == num_partidos:
        full_input = full_input.apply(pd.to_numeric, errors="coerce").fillna(0)
        full_input["Dobles Realizados"] = (full_input["Puntos"] - (full_input["Triples"] * 3) - full_input["Libres"]) / 2
        full_input["Dobles Intentados"] = full_input["FGA"] - full_input["3PT INT"]
        st.markdown("### 🔍 Análisis completo")
        st.dataframe(full_input, use_container_width=True)
