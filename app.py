
import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(page_title="NBA Stats Analyzer", layout="centered")

# Mostrar pantalla de bienvenida primero
if "ingreso" not in st.session_state:
    st.session_state["ingreso"] = False

if not st.session_state["ingreso"]:
    st.title("🏀 NBA Stats Analyzer")
    st.markdown("📊 *Análisis, estadísticas y apuestas del día en un solo lugar*")

    st.markdown("---")
    archivo_demo = st.file_uploader("Subí el archivo de la Apuesta del Día para continuar (Excel)", type=["xlsx"], key="bienvenida")
    if archivo_demo:
        try:
            wb = openpyxl.load_workbook(archivo_demo, data_only=True)
            hoja = wb.active
            fecha_actual = hoja["A1"].value
            if fecha_actual:
                st.markdown(f"📅 Última actualización: **{fecha_actual}**")
        except:
            st.warning("No se pudo leer la fecha desde el archivo.")

    if st.button("Ingresar al análisis"):
        st.session_state["ingreso"] = True

    st.markdown("---")
    st.caption("Creado por Blaink 🧠")
    st.stop()

# App principal
st.title("🏀 NBA Stats Analyzer")
tabs = st.tabs([
    "Dobles Realizados",
    "Dobles Intentados",
    "Estadísticas Completas",
    "Apuesta del Día"
])

num_partidos = 10

# ---------- TAB 1 ----------
with tabs[0]:
    st.subheader("🎯 Dobles Realizados")
    df_manual = pd.DataFrame({
        "Puntos": [None]*num_partidos,
        "Triples": [None]*num_partidos,
        "Libres": [None]*num_partidos
    })
    data_input = st.data_editor(df_manual, num_rows="fixed", use_container_width=True, key="manual_realizados")

    if data_input.dropna().shape[0] == num_partidos:
        cols = ["Puntos", "Triples", "Libres"]
        data_input[cols] = data_input[cols].apply(pd.to_numeric, errors="coerce").fillna(0)
        data_input["Dobles"] = (data_input["Puntos"] - (data_input["Triples"] * 3) - data_input["Libres"]) / 2
        st.markdown("### ✅ Dobles Calculados")
        st.dataframe(data_input, use_container_width=True)

        linea = st.number_input("Ingresá la línea a evaluar (dobles realizados)", min_value=0.0, step=0.5, key="linea_realizados")
        aciertos = (data_input["Dobles"] > linea).sum()
        st.markdown(f"**Aciertos sobre la línea:** {aciertos} / {len(data_input)}")

# ---------- TAB 2 ----------
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

# ---------- TAB 3 ----------
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

# ---------- TAB 4 ----------
with tabs[3]:
    st.subheader("📋 Apuesta del Día")

    archivo = st.file_uploader("Subí el archivo Excel con las apuestas", type=["xlsx"], key="apuestas")
    if archivo:
        try:
            df = pd.read_excel(archivo)
            st.success("✅ Apuestas cargadas correctamente")
            st.dataframe(df, use_container_width=True)
        except:
            st.error("❌ Error al leer el archivo. Asegurate que sea formato Excel (.xlsx)")
