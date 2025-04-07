
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NBA Stats Analyzer", layout="wide")

st.markdown("""<style>
    .stDataFrame tbody td {
        text-align: center;
    }
</style>""", unsafe_allow_html=True)

# Página de changelog
if "show_changelog" not in st.session_state:
    st.session_state.show_changelog = True

if st.session_state.show_changelog:
    st.title("📢 Actualizaciones Recientes")
    st.markdown("- ✅ Cálculo corregido en F.G.M")
    st.markdown("- ✅ F.G.A incorporado con dobles intentados")
    st.markdown("- ✅ Datos centrados en las tablas")
    if st.button("Ingresar a la app"):
        st.session_state.show_changelog = False
    st.stop()

# Sidebar de navegación
page = st.sidebar.radio("Navegación", ["TIROS DE CAMPO ACERTADOS (F.G.M)", "TIROS DE CAMPO INTENTADOS (F.G.A)", "Apuesta del Día"])

# Inicializar datos
if "data_fgm" not in st.session_state:
    st.session_state.data_fgm = pd.DataFrame({
        "Puntos": [0]*10,
        "Triples": [0]*10,
        "Libres": [0]*10
    })

if "data_fga" not in st.session_state:
    st.session_state.data_fga = pd.DataFrame({
        "FGA (Tiros de campo intentados)": [0]*10,
        "Triples intentados": [0]*10
    })

# Página F.G.M
if page == "TIROS DE CAMPO ACERTADOS (F.G.M)":
    st.title("TIROS DE CAMPO ACERTADOS (F.G.M)")
    tipo = st.selectbox("Tipo de línea a calcular", ["Dobles Acertados", "Triples Acertados", "Libres Acertados", "Puntos Acertados"])

    edited_df = st.data_editor(st.session_state.data_fgm, use_container_width=True, num_rows="fixed", key="fgm_editor")
    st.session_state.data_fgm = edited_df.copy()

    if st.button("🧹 Limpiar tabla (FGM)"):
        st.session_state.data_fgm.loc[:, :] = 0
        st.rerun()

    linea = st.number_input("Línea a evaluar", min_value=0.0, step=0.5, key="linea_fgm")
    cantidad = st.slider("Cantidad de partidos a analizar", 3, 30, 10, key="slider_fgm")

    if st.button("Calcular línea (FGM)"):
        try:
            df = st.session_state.data_fgm.copy()
            df = df.head(cantidad).apply(pd.to_numeric, errors="coerce")

            if tipo == "Dobles Acertados":
                df["Dobles"] = (df["Puntos"] - df["Triples"] * 3 - df["Libres"]) / 2
                valores = df["Dobles"]
            elif tipo == "Triples Acertados":
                valores = df["Triples"]
            elif tipo == "Libres Acertados":
                valores = df["Libres"]
            else:
                valores = df["Puntos"]

            aciertos = (valores > linea).sum()
            st.success(f"Aciertos: {aciertos} / {len(valores)}")
            st.bar_chart(valores)
        except Exception as e:
            st.error(f"Error al calcular: {e}")

# Página F.G.A
elif page == "TIROS DE CAMPO INTENTADOS (F.G.A)":
    st.title("TIROS DE CAMPO INTENTADOS (F.G.A)")
    tipo = st.selectbox("Tipo de línea a calcular", ["Tiros de campo intentados", "Triples intentados", "Dobles intentados"])

    edited_df = st.data_editor(st.session_state.data_fga, use_container_width=True, num_rows="fixed", key="fga_editor")
    st.session_state.data_fga = edited_df.copy()

    if st.button("🧹 Limpiar tabla (FGA)"):
        st.session_state.data_fga.loc[:, :] = 0
        st.rerun()

    linea = st.number_input("Línea a evaluar", min_value=0.0, step=0.5, key="linea_fga")
    cantidad = st.slider("Cantidad de partidos a analizar", 3, 30, 10, key="slider_fga")

    if st.button("Calcular línea (FGA)"):
        try:
            df2 = st.session_state.data_fga.copy()
            df2 = df2.head(cantidad).apply(pd.to_numeric, errors="coerce")

            if tipo == "Dobles intentados":
                df2["Dobles intentados"] = df2["FGA (Tiros de campo intentados)"] - df2["Triples intentados"]
                valores = df2["Dobles intentados"]
            elif tipo == "Triples intentados":
                valores = df2["Triples intentados"]
            else:
                valores = df2["FGA (Tiros de campo intentados)"]

            aciertos = (valores > linea).sum()
            st.success(f"Aciertos: {aciertos} / {len(valores)}")
            st.bar_chart(valores)
        except Exception as e:
            st.error(f"Error al calcular: {e}")

# Página Apuesta del Día
elif page == "Apuesta del Día":
    st.title("📋 Apuesta del Día")
    st.markdown("""
    Esta apuesta fue actualizada manualmente por **@BlainkEiou**.  
    📬 Ante cualquier duda o sugerencia, contactame por Telegram: [@BlainkEiou](https://t.me/BlainkEiou)
    """)
    if os.path.exists("apuesta_dia.xlsx"):
        df_apuesta = pd.read_excel("apuesta_dia.xlsx")
        st.dataframe(df_apuesta, use_container_width=True)
    else:
        st.warning("⚠️ No se encontró el archivo 'apuesta_dia.xlsx'. Asegurate de colocarlo en la carpeta raíz.")
