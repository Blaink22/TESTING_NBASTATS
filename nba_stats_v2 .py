
import streamlit as st
import pandas as pd

st.set_page_config(page_title="NBA Stats Analyzer", layout="wide")

# Pantalla de changelog inicial
if "show_changelog" not in st.session_state:
    st.session_state.show_changelog = True

if st.session_state.show_changelog:
    st.title("📢 Actualizaciones Recientes")
    st.markdown("- ✅ Estilo visual mejorado (modo profesional)")
    st.markdown("- ✅ F.G.M y F.G.A con tablas restauradas")
    st.markdown("- ✅ Selector de tipo de línea: dobles, triples, puntos, libres")
    st.markdown("- ✅ Selección de cantidad de partidos: 10, 20 o personalizado")
    st.markdown("- ✅ Botón para limpiar los datos")
    st.markdown("- ✅ Acceso a la Apuesta del Día")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ingresar a la aplicación"):
            st.session_state.show_changelog = False
    with col2:
        if st.button("Ir a Apuesta del Día"):
            st.switch_page("apuesta_dia")
    st.stop()

# Función para elegir cantidad de partidos
def seleccionar_partidos():
    tipo = st.radio("¿Cuántos partidos querés analizar?", ["Últimos 10", "Últimos 20", "Personalizado"])
    if tipo == "Últimos 10":
        return 10
    elif tipo == "Últimos 20":
        return 20
    else:
        return st.slider("Elegí la cantidad de partidos", min_value=3, max_value=30, value=10)

# Función para ingresar datos en F.G.M
def ingresar_datos_fgm(num_partidos):
    df = pd.DataFrame({
        "Puntos": [None]*num_partidos,
        "Triples": [None]*num_partidos,
        "Libres": [None]*num_partidos
    })
    return st.data_editor(df, use_container_width=True, num_rows="fixed", key="fgm_editor")

# Función para ingresar datos en F.G.A
def ingresar_datos_fga(num_partidos):
    df = pd.DataFrame({
        "FGA": [None]*num_partidos,
        "Triples Intentados": [None]*num_partidos
    })
    return st.data_editor(df, use_container_width=True, num_rows="fixed", key="fga_editor")

# Función para calcular aciertos
def calcular_aciertos(df, tipo, linea):
    if tipo == "Dobles Acertados":
        valores = (df["Puntos"] - (df["Triples"] * 3) - df["Libres"]) / 2
    elif tipo == "Triples Acertados":
        valores = df["Triples"]
    elif tipo == "Puntos Acertados":
        valores = df["Puntos"]
    elif tipo == "Libres Acertados":
        valores = df["Libres"]
    elif tipo == "Tiros de Campo Intentados":
        valores = df["FGA"]
    elif tipo == "Triples Intentados":
        valores = df["Triples Intentados"]
    elif tipo == "Dobles Intentados":
        valores = df["FGA"] - df["Triples Intentados"]
    else:
        return 0, []
    aciertos = (valores > linea).sum()
    return aciertos, valores

# Selector de pestañas
seccion = st.selectbox("📂 Elegí una sección", ["TIROS DE CAMPO ACERTADOS (F.G.M)", "TIROS DE CAMPO INTENTADOS (F.G.A)"])

# Seleccionar cantidad de partidos
num_partidos = seleccionar_partidos()

if seccion == "TIROS DE CAMPO ACERTADOS (F.G.M)":
    st.subheader("🎯 Análisis de Tiros Acertados (F.G.M)")
    datos = ingresar_datos_fgm(num_partidos)
    tipo = st.selectbox("Tipo de línea a calcular", ["Dobles Acertados", "Triples Acertados", "Puntos Acertados", "Libres Acertados"])
    if st.button("🧹 Limpiar tabla", key="limpiar_fgm"):
        st.experimental_rerun()
else:
    st.subheader("🏹 Análisis de Tiros Intentados (F.G.A)")
    datos = ingresar_datos_fga(num_partidos)
    tipo = st.selectbox("Tipo de línea a calcular", ["Tiros de Campo Intentados", "Triples Intentados", "Dobles Intentados"])
    if st.button("🧹 Limpiar tabla", key="limpiar_fga"):
        st.experimental_rerun()

linea = st.number_input("📏 Ingresá la línea a evaluar", min_value=0.0, step=0.5)

if st.button("Calcular Línea"):
    if datos.dropna().shape[0] < 3:
        st.warning("⚠️ Ingresá al menos 3 filas completas.")
    else:
        aciertos, valores = calcular_aciertos(datos, tipo, linea)
        st.success(f"✅ Aciertos: {aciertos} / {num_partidos}")
        st.bar_chart(valores, use_container_width=True)
