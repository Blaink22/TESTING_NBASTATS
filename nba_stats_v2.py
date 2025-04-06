
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NBA Stats Analyzer", layout="wide")

# Pantalla de changelog
if "show_changelog" not in st.session_state:
    st.session_state.show_changelog = True

if st.session_state.show_changelog:
    st.title("📢 Actualizaciones Recientes")
    st.markdown("- Sección 'Apuesta del Día' restaurada (Excel precargado)")
    st.markdown("- Limpieza de tabla corregida")
    st.markdown("- Soporte completo para FGM y FGA sin errores")
    if st.button("Ingresar a la app"):
        st.session_state.show_changelog = False
    if st.button("Ir a Apuesta del Día"):
        st.session_state.page = "Apuesta del Día"
        st.rerun()
    st.stop()

# Página principal
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a:", ["TIROS DE CAMPO ACERTADOS (F.G.M)", "TIROS DE CAMPO INTENTADOS (F.G.A)", "Apuesta del Día"])

# Inicialización de datos
if "data_fgm" not in st.session_state:
    st.session_state.data_fgm = [{"Puntos": 0, "Triples": 0, "Libres": 0} for _ in range(10)]
if "data_fga" not in st.session_state:
    st.session_state.data_fga = [{"FGA": 0, "Triples intentados": 0} for _ in range(10)]

def reset_data(section):
    if section == "fgm":
        st.session_state.data_fgm = [{"Puntos": 0, "Triples": 0, "Libres": 0} for _ in range(10)]
    elif section == "fga":
        st.session_state.data_fga = [{"FGA": 0, "Triples intentados": 0} for _ in range(10)]
    st.rerun()

if page == "TIROS DE CAMPO ACERTADOS (F.G.M)":
    st.title("TIROS DE CAMPO ACERTADOS (F.G.M)")
    tipo = st.selectbox("Tipo de línea a calcular", ["Dobles Acertados", "Triples Acertados", "Libres Acertados", "Puntos Acertados"])
    df = pd.DataFrame(st.session_state.data_fgm)
    st.data_editor(df, key="fgm_editor", use_container_width=True)
    if st.button("🧹 Limpiar tabla (FGM)"):
        reset_data("fgm")
    linea = st.number_input("Línea", min_value=0.0, step=0.5)
    cantidad = st.slider("Cantidad de partidos", 3, 30, 10)
    if st.button("Calcular Línea (FGM)"):
        try:
            if tipo == "Dobles Acertados":
                df["Dobles"] = (df["Puntos"] - df["Triples"] * 3 - df["Libres"]) / 2
                valores = df["Dobles"].head(cantidad)
            elif tipo == "Triples Acertados":
                valores = df["Triples"].head(cantidad)
            elif tipo == "Libres Acertados":
                valores = df["Libres"].head(cantidad)
            else:
                valores = df["Puntos"].head(cantidad)
            aciertos = sum(valores > linea)
            st.success(f"Aciertos: {aciertos} / {len(valores)}")
            st.bar_chart(valores)
        except Exception as e:
            st.error(f"Error al calcular: {e}")

elif page == "TIROS DE CAMPO INTENTADOS (F.G.A)":
    st.title("TIROS DE CAMPO INTENTADOS (F.G.A)")
    tipo = st.selectbox("Tipo de línea a calcular", ["Tiros de campo intentados", "Triples intentados", "Dobles intentados"])
    df2 = pd.DataFrame(st.session_state.data_fga)
    st.data_editor(df2, key="fga_editor", use_container_width=True)
    if st.button("🧹 Limpiar tabla (FGA)"):
        reset_data("fga")
    linea = st.number_input("Línea", min_value=0.0, step=0.5, key="linea_fga")
    cantidad = st.slider("Cantidad de partidos", 3, 30, 10, key="partidos_fga")
    if st.button("Calcular Línea (FGA)"):
        try:
            if tipo == "Dobles intentados":
                df2["Dobles intentados"] = df2["FGA"] - df2["Triples intentados"]
                valores = df2["Dobles intentados"].head(cantidad)
            elif tipo == "Triples intentados":
                valores = df2["Triples intentados"].head(cantidad)
            else:
                valores = df2["FGA"].head(cantidad)
            aciertos = sum(valores > linea)
            st.success(f"Aciertos: {aciertos} / {len(valores)}")
            st.bar_chart(valores)
        except Exception as e:
            st.error(f"Error al calcular: {e}")

elif page == "Apuesta del Día":
    st.title("📋 Apuesta del Día")
    if os.path.exists("apuesta_dia.xlsx"):
        df_apuesta = pd.read_excel("apuesta_dia.xlsx")
        st.dataframe(df_apuesta, use_container_width=True)
    else:
        st.warning("⚠️ No se encontró el archivo 'apuesta_dia.xlsx'. Asegurate de colocarlo en la carpeta raíz.")
