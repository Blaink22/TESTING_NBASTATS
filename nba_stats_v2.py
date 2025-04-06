
import streamlit as st
import pandas as pd

# Pantalla de advertencia tipo changelog (solo se muestra al inicio)
if "bienvenida_mostrada" not in st.session_state:
    st.session_state.bienvenida_mostrada = False

if not st.session_state.bienvenida_mostrada:
    st.markdown("## 📢 Novedades")
    st.markdown("- Nuevo diseño más profesional 🏀")
    st.markdown("- Secciones renombradas: **F.G.M** y **F.G.A**")
    st.markdown("- Cálculo inteligente según tipo de estadística")
    st.markdown("- Opción para elegir cantidad de partidos a analizar")
    st.markdown("---")
    if st.button("Ingresar a la aplicación"):
        st.session_state.bienvenida_mostrada = True
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

# Función para ingresar datos
def ingresar_datos(num_partidos):
    st.markdown("### 📋 Ingresá los datos:")
    df = pd.DataFrame({
        "Puntos": [None]*num_partidos,
        "Triples": [None]*num_partidos,
        "Libres": [None]*num_partidos,
        "FGA": [None]*num_partidos,
        "FGM": [None]*num_partidos
    })
    return st.data_editor(df, use_container_width=True, num_rows="fixed")

# Cálculo de aciertos basado en tipo
def calcular_aciertos(df, tipo, linea):
    if tipo == "Dobles Acertados":
        valores = (df["Puntos"] - (df["Triples"] * 3) - df["Libres"]) / 2
    elif tipo == "Triples Acertados":
        valores = df["Triples"]
    elif tipo == "Puntos Acertados":
        valores = df["Puntos"]
    elif tipo == "Libres Acertados":
        valores = df["Libres"]
    elif tipo == "F.G.M":
        valores = df["FGM"]
    elif tipo == "F.G.A":
        valores = df["FGA"]
    else:
        return 0, []
    aciertos = (valores > linea).sum()
    return aciertos, valores

# Título principal
st.title("🏀 NBA Stats Analyzer (Versión Mejorada)")

# Navegación por pestañas
seccion = st.selectbox("Elegí una sección", ["TIROS DE CAMPO ACERTADOS (F.G.M)", "TIROS DE CAMPO INTENTADOS (F.G.A)"])

# Determinar partidos
num_partidos = seleccionar_partidos()

# Ingreso de datos
datos = ingresar_datos(num_partidos)

# Selección de tipo de análisis
st.markdown("### 🎯 Seleccioná qué querés calcular")
tipo = st.selectbox("Tipo de estadística", ["Dobles Acertados", "Triples Acertados", "Puntos Acertados", "Libres Acertados"] if seccion == "TIROS DE CAMPO ACERTADOS (F.G.M)" else ["F.G.A"])

# Línea objetivo
linea = st.number_input("📏 Ingresá la línea a evaluar", min_value=0.0, step=0.5)

# Botón de cálculo
if st.button("Calcular línea"):
    if datos.dropna().shape[0] < 3:
        st.warning("⚠️ Ingresá al menos 3 filas completas para calcular.")
    else:
        tipo_real = tipo if tipo != "F.G.A" else "F.G.A"
        aciertos, valores = calcular_aciertos(datos, tipo_real, linea)
        st.success(f"✅ Aciertos: {aciertos} / {num_partidos}")
        st.bar_chart(valores, use_container_width=True)
