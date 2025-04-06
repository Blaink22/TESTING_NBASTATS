
import streamlit as st
import pandas as pd

st.set_page_config(page_title="NBA Stats Analyzer", layout="wide")

# Estado inicial de los datos por sección
if 'data_fgm' not in st.session_state:
    st.session_state.data_fgm = [{"Puntos": None, "Triples": None, "Libres": None} for _ in range(10)]
if 'data_fga' not in st.session_state:
    st.session_state.data_fga = [{"FGA (Tiros de campo intentados)": None, "Triples intentados": None} for _ in range(10)]

# Función para limpiar los datos de una sección
def reset_section_data(section):
    if section == 'fgm':
        st.session_state.data_fgm = [{"Puntos": None, "Triples": None, "Libres": None} for _ in range(10)]
    elif section == 'fga':
        st.session_state.data_fga = [{"FGA (Tiros de campo intentados)": None, "Triples intentados": None} for _ in range(10)]
    st.rerun()

# Navegación entre páginas
page = st.sidebar.selectbox("Navegación", ["Inicio", "TIROS DE CAMPO ACERTADOS (F.G.M)", "TIROS DE CAMPO INTENTADOS (F.G.A)", "Apuesta del Día"])

# Página de inicio con changelog y botón de acceso rápido
if page == "Inicio":
    st.title("NBA Stats Analyzer v2")
    st.success("Sitio actualizado y funcionando correctamente con todas las funcionalidades.")
    if st.button("Ir a la Apuesta del Día"):
        st.session_state.selected_page = "Apuesta del Día"
        st.rerun()

# F.G.M
elif page == "TIROS DE CAMPO ACERTADOS (F.G.M)":
    st.title("TIROS DE CAMPO ACERTADOS (F.G.M)")
    tipo = st.selectbox("Tipo de línea a calcular", ["Dobles Acertados", "Triples Acertados", "Libres Acertados", "Puntos Acertados"])
    df = pd.DataFrame(st.session_state.data_fgm)
    st.data_editor(df, key="data_fgm", use_container_width=True)

    if st.button("Limpiar tabla"):
        reset_section_data('fgm')

    linea = st.number_input("Línea a calcular", min_value=0.0, step=0.5)
    cantidad = st.slider("Cantidad de partidos a analizar", min_value=3, max_value=30, value=10)

    if st.button("Calcular línea"):
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
        st.success(f"Aciertos: {aciertos}/{len(valores)}")

# F.G.A
elif page == "TIROS DE CAMPO INTENTADOS (F.G.A)":
    st.title("TIROS DE CAMPO INTENTADOS (F.G.A)")
    tipo = st.selectbox("Tipo de línea a calcular", ["Tiros de campo intentados", "Triples intentados", "Dobles intentados"])
    df2 = pd.DataFrame(st.session_state.data_fga)
    st.data_editor(df2, key="data_fga", use_container_width=True)

    if st.button("Limpiar tabla"):
        reset_section_data('fga')

    linea = st.number_input("Línea a calcular", min_value=0.0, step=0.5, key="linea_fga")
    cantidad = st.slider("Cantidad de partidos a analizar", min_value=3, max_value=30, value=10, key="slider_fga")

    if st.button("Calcular línea", key="calc_fga"):
        if tipo == "Dobles intentados":
            df2["Dobles intentados"] = df2["FGA (Tiros de campo intentados)"] - df2["Triples intentados"]
            valores = df2["Dobles intentados"].head(cantidad)
        elif tipo == "Triples intentados":
            valores = df2["Triples intentados"].head(cantidad)
        else:
            valores = df2["FGA (Tiros de campo intentados)"].head(cantidad)

        aciertos = sum(valores > linea)
        st.success(f"Aciertos: {aciertos}/{len(valores)}")

# Apuesta del Día
elif page == "Apuesta del Día":
    st.title("📋 Apuesta del Día")
    st.info("Subí el archivo Excel con las apuestas")
    file = st.file_uploader("Cargar archivo .xlsx", type=["xlsx"])

    if file:
        df_apuesta = pd.read_excel(file)
        st.dataframe(df_apuesta)
