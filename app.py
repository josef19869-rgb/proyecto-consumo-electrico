
# ============================================================
# app.py — Análisis de Consumo Eléctrico
# Proyecto Final — Ciencia de Datos
# Área: Ingeniería / Tecnología
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# ── CONFIGURACIÓN DE PÁGINA ──────────────────────────────────
st.set_page_config(
    page_title="⚡ Análisis de Consumo Eléctrico",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── ESTILOS CSS PERSONALIZADOS ───────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0077b6;
        text-align: center;
        padding: 10px 0;
    }
    .subtitle {
        font-size: 1rem;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f0f7ff;
        border-left: 4px solid #0077b6;
        padding: 10px 15px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .section-header {
        background: linear-gradient(90deg, #0077b6, #00b4d8);
        color: white;
        padding: 8px 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── TÍTULO PRINCIPAL ─────────────────────────────────────────
st.markdown('<div class="main-title">⚡ Análisis de Consumo Eléctrico y Energía</div>',
            unsafe_allow_html=True)
st.markdown('<div class="subtitle">Proyecto Final · Ingeniería / Tecnología · Ciencia de Datos</div>',
            unsafe_allow_html=True)
st.markdown("---")

# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/lightning-bolt.png", width=80)
    st.header("📂 Cargar Dataset")
    archivo = st.file_uploader(
        "Sube tu archivo CSV aquí",
        type=["csv"],
        help="El dataset debe estar en formato CSV"
    )
    st.markdown("---")

# ── FUNCIÓN DE CARGA ─────────────────────────────────────────
@st.cache_data
def cargar_datos(archivo):
    df = pd.read_csv(archivo)
    return df

# ── PANTALLA DE BIENVENIDA (sin dataset) ─────────────────────
if archivo is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("👈 **Comienza subiendo tu dataset CSV en el panel izquierdo**")
        st.markdown("""
        ### 🗂️ ¿Qué puedes analizar con esta app?

        | Sección | Contenido |
        |---|---|
        | 1️⃣ Exploración Inicial | Dimensiones, tipos de datos, valores nulos |
        | 2️⃣ Estadísticas | Media, mediana, desviación estándar, percentiles |
        | 3️⃣ Visualizaciones | Gráficos de línea, barras e histogramas |
        | 4️⃣ Correlaciones | Mapa de calor y dispersión entre variables |
        | 5️⃣ Filtros | Segmentación interactiva y descarga de datos |
        | 6️⃣ Conclusiones | Hallazgos y recomendaciones del análisis |

        ---
        **Dataset recomendado:** Consumo eléctrico con columnas de
        fecha, hora, potencia, voltaje y/o intensidad.
        """)

# ── APP PRINCIPAL (con dataset) ──────────────────────────────
else:
    df = cargar_datos(archivo)

    # Identificar columnas numéricas y categóricas
    numericas = df.select_dtypes(include="number").columns.tolist()
    categoricas = df.select_dtypes(include="object").columns.tolist()

    # ── MENÚ DE NAVEGACIÓN ───────────────────────────────────
    with st.sidebar:
        st.success(f"✅ Dataset cargado: {df.shape[0]:,} filas")
        st.markdown("---")
        st.header("📌 Navegación")
        seccion = st.radio("Selecciona una sección:", [
            "1️⃣  Exploración Inicial",
            "2️⃣  Estadísticas Descriptivas",
            "3️⃣  Visualizaciones",
            "4️⃣  Análisis de Correlación",
            "5️⃣  Filtros Interactivos",
            "6️⃣  Conclusiones"
        ])

    # ════════════════════════════════════════════════════════
    # SECCIÓN 1 — EXPLORACIÓN INICIAL
    # ════════════════════════════════════════════════════════
    if "1️⃣" in seccion:
        st.markdown('<div class="section-header"><h3>1️⃣ Exploración Inicial del Dataset</h3></div>',
                    unsafe_allow_html=True)

        # Métricas principales
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📊 Filas", f"{df.shape[0]:,}")
        c2.metric("📋 Columnas", df.shape[1])
        c3.metric("❌ Valores Nulos", df.isnull().sum().sum())
        c4.metric("🔢 Col. Numéricas", len(numericas))

        st.markdown("---")

        # Vista previa
        st.subheader("🔍 Vista previa del dataset")
        n_filas = st.slider("Número de filas a mostrar:", 5, 100, 10, step=5)
        st.dataframe(df.head(n_filas), use_container_width=True)

        # Información de columnas
        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("📋 Información de columnas")
            info_df = pd.DataFrame({
                "Columna": df.columns,
                "Tipo": df.dtypes.values.astype(str),
                "Nulos": df.isnull().sum().values,
                "% Nulos": (df.isnull().sum().values / len(df) * 100).round(2),
                "Únicos": df.nunique().values
            })
            st.dataframe(info_df, use_container_width=True)

        with col_b:
            st.subheader("❌ Valores nulos por columna")
            nulos = df.isnull().sum()
            nulos = nulos[nulos > 0]
            if len(nulos) > 0:
                fig, ax = plt.subplots(figsize=(6, 4))
                nulos.plot(kind="barh", ax=ax, color="#e63946")
                ax.set_title("Columnas con valores nulos")
                ax.set_xlabel("Cantidad de nulos")
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            else:
                st.success("✅ ¡El dataset no tiene valores nulos!")

    # ════════════════════════════════════════════════════════
    # SECCIÓN 2 — ESTADÍSTICAS DESCRIPTIVAS
    # ════════════════════════════════════════════════════════
    elif "2️⃣" in seccion:
        st.markdown('<div class="section-header"><h3>2️⃣ Estadísticas Descriptivas</h3></div>',
                    unsafe_allow_html=True)

        st.subheader("📈 Resumen estadístico completo")
        st.dataframe(
            df[numericas].describe().T.style.format("{:.3f}").background_gradient(
                cmap="Blues", subset=["mean", "std"]
            ),
            use_container_width=True
        )

        st.markdown("---")

        col_izq, col_der = st.columns(2)

        with col_izq:
            st.subheader("📊 Distribución de variable")
            if numericas:
                var_hist = st.selectbox("Selecciona la variable:", numericas, key="hist_var")
                bins = st.slider("Número de barras:", 10, 100, 30)
                fig = px.histogram(
                    df, x=var_hist, nbins=bins,
                    title=f"Distribución de {var_hist}",
                    color_discrete_sequence=["#0077b6"],
                    marginal="box"
                )
                fig.update_layout(bargap=0.05)
                st.plotly_chart(fig, use_container_width=True)

        with col_der:
            st.subheader("📦 Boxplot (detección de outliers)")
            if numericas:
                var_box = st.selectbox("Selecciona la variable:", numericas, key="box_var")
                fig2 = px.box(
                    df, y=var_box,
                    title=f"Boxplot de {var_box}",
                    color_discrete_sequence=["#00b4d8"],
                    points="outliers"
                )
                st.plotly_chart(fig2, use_container_width=True)

        # Tabla de percentiles
        st.markdown("---")
        st.subheader("📐 Percentiles por variable")
        percentiles = df[numericas].quantile([0.10, 0.25, 0.50, 0.75, 0.90]).T
        percentiles.columns = ["P10", "P25", "P50 (Mediana)", "P75", "P90"]
        st.dataframe(percentiles.style.format("{:.3f}").background_gradient(cmap="YlOrRd"),
                     use_container_width=True)

    # ════════════════════════════════════════════════════════
    # SECCIÓN 3 — VISUALIZACIONES
    # ════════════════════════════════════════════════════════
    elif "3️⃣" in seccion:
        st.markdown('<div class="section-header"><h3>3️⃣ Visualizaciones de Consumo Eléctrico</h3></div>',
                    unsafe_allow_html=True)

        # Gráfico de línea temporal
        st.subheader("📈 Evolución temporal del consumo")
        col_x = st.selectbox("Eje X (columna de tiempo/secuencia):", df.columns.tolist())
        col_y = st.selectbox("Eje Y (variable de consumo):", numericas)

        muestra = st.slider("Mostrar primeros N registros:", 100, len(df), min(1000, len(df)), step=100)
        df_muestra = df.head(muestra)

        fig_linea = px.line(
            df_muestra, x=col_x, y=col_y,
            title=f"Evolución de {col_y} a lo largo de {col_x}",
            color_discrete_sequence=["#e63946"],
            template="plotly_white"
        )
        fig_linea.update_traces(line_width=1.5)
        st.plotly_chart(fig_linea, use_container_width=True)

        st.markdown("---")
        col_l, col_r = st.columns(2)

        with col_l:
            st.subheader("📊 Promedio por categoría")
            if categoricas:
                cat_sel = st.selectbox("Variable categórica:", categoricas)
                val_sel = st.selectbox("Variable de valor:", numericas, key="barra_num")
                df_agr = df.groupby(cat_sel)[val_sel].mean().reset_index().sort_values(val_sel, ascending=False)
                fig_bar = px.bar(
                    df_agr, x=cat_sel, y=val_sel,
                    title=f"Promedio de {val_sel} por {cat_sel}",
                    color=val_sel,
                    color_continuous_scale="Blues",
                    template="plotly_white"
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No hay columnas categóricas en el dataset.")

        with col_r:
            st.subheader("🔢 Comparación múltiple")
            vars_multi = st.multiselect(
                "Selecciona variables a comparar:",
                numericas,
                default=numericas[:min(3, len(numericas))]
            )
            if vars_multi:
                df_norm = df[vars_multi].copy()
                for col in vars_multi:
                    rng = df_norm[col].max() - df_norm[col].min()
                    if rng != 0:
                        df_norm[col] = (df_norm[col] - df_norm[col].min()) / rng
                fig_multi = px.line(
                    df_norm.head(500),
                    title="Variables normalizadas (0-1) — primeros 500 registros",
                    template="plotly_white"
                )
                st.plotly_chart(fig_multi, use_container_width=True)

    # ════════════════════════════════════════════════════════
    # SECCIÓN 4 — CORRELACIÓN
    # ════════════════════════════════════════════════════════
    elif "4️⃣" in seccion:
        st.markdown('<div class="section-header"><h3>4️⃣ Análisis de Correlación</h3></div>',
                    unsafe_allow_html=True)

        if len(numericas) >= 2:
            col_izq, col_der = st.columns([3, 2])

            with col_izq:
                st.subheader("🌡️ Mapa de calor de correlaciones")
                metodo = st.radio("Método:", ["pearson", "spearman", "kendall"], horizontal=True)
                corr_matrix = df[numericas].corr(method=metodo)

                fig_heat, ax = plt.subplots(figsize=(10, 7))
                mask = None
                sns.heatmap(
                    corr_matrix, annot=True, fmt=".2f",
                    cmap="RdYlBu_r", ax=ax,
                    linewidths=0.5, linecolor="white",
                    vmin=-1, vmax=1,
                    annot_kws={"size": 9}
                )
                ax.set_title(f"Matriz de Correlación ({metodo.capitalize()})", pad=15)
                plt.tight_layout()
                st.pyplot(fig_heat)
                plt.close()

            with col_der:
                st.subheader("📊 Correlaciones más fuertes")
                corr_pairs = corr_matrix.unstack().reset_index()
                corr_pairs.columns = ["Variable 1", "Variable 2", "Correlación"]
                corr_pairs = corr_pairs[corr_pairs["Variable 1"] != corr_pairs["Variable 2"]]
                corr_pairs["Abs"] = corr_pairs["Correlación"].abs()
                corr_pairs = corr_pairs.sort_values("Abs", ascending=False).drop_duplicates(subset=["Abs"])
                st.dataframe(
                    corr_pairs[["Variable 1", "Variable 2", "Correlación"]].head(10).style.format(
                        {"Correlación": "{:.3f}"}
                    ).background_gradient(cmap="RdYlGn", subset=["Correlación"]),
                    use_container_width=True
                )

            st.markdown("---")
            st.subheader("🔵 Diagrama de dispersión")
            c1, c2 = st.columns(2)
            var_x = c1.selectbox("Variable X:", numericas, key="disp_x")
            var_y = c2.selectbox("Variable Y:", numericas, key="disp_y", index=min(1, len(numericas)-1))

            color_col = None
            if categoricas:
                color_col = st.selectbox("Color por categoría (opcional):", ["Ninguno"] + categoricas)
                if color_col == "Ninguno":
                    color_col = None

            fig_disp = px.scatter(
                df.sample(min(2000, len(df))),
                x=var_x, y=var_y,
                color=color_col,
                title=f"Dispersión: {var_x} vs {var_y}",
                trendline="ols",
                opacity=0.6,
                template="plotly_white"
            )
            st.plotly_chart(fig_disp, use_container_width=True)
        else:
            st.warning("Se necesitan al menos 2 columnas numéricas para el análisis de correlación.")

    # ════════════════════════════════════════════════════════
    # SECCIÓN 5 — FILTROS INTERACTIVOS
    # ════════════════════════════════════════════════════════
    elif "5️⃣" in seccion:
        st.markdown('<div class="section-header"><h3>5️⃣ Filtros Interactivos</h3></div>',
                    unsafe_allow_html=True)

        st.info("Usa los filtros para segmentar los datos según tus criterios de análisis.")

        df_filtrado = df.copy()

        # Filtros numéricos
        st.subheader("🔢 Filtros numéricos")
        cols_filtro = st.multiselect(
            "Selecciona columnas para filtrar:",
            numericas,
            default=numericas[:min(2, len(numericas))]
        )

        filtros_activos = {}
        for col in cols_filtro:
            min_v = float(df[col].min())
            max_v = float(df[col].max())
            rango = st.slider(
                f"Rango de **{col}**:",
                min_v, max_v, (min_v, max_v),
                key=f"filtro_{col}",
                format="%.2f"
            )
            filtros_activos[col] = rango
            df_filtrado = df_filtrado[
                (df_filtrado[col] >= rango[0]) & (df_filtrado[col] <= rango[1])
            ]

        # Filtros categóricos
        if categoricas:
            st.subheader("🏷️ Filtros categóricos")
            for cat in categoricas[:3]:
                opciones = df[cat].dropna().unique().tolist()
                seleccion = st.multiselect(
                    f"Filtrar por **{cat}**:",
                    opciones, default=opciones,
                    key=f"cat_{cat}"
                )
                if seleccion:
                    df_filtrado = df_filtrado[df_filtrado[cat].isin(seleccion)]

        # Resultados del filtro
        st.markdown("---")
        pct = len(df_filtrado) / len(df) * 100
        c1, c2, c3 = st.columns(3)
        c1.metric("📊 Registros originales", f"{len(df):,}")
        c2.metric("✅ Registros filtrados", f"{len(df_filtrado):,}")
        c3.metric("📉 Porcentaje seleccionado", f"{pct:.1f}%")

        if len(df_filtrado) > 0:
            st.dataframe(df_filtrado, use_container_width=True)

            # Estadísticas del subconjunto filtrado
            if numericas:
                st.subheader("📈 Estadísticas del subconjunto filtrado")
                st.dataframe(
                    df_filtrado[numericas].describe().T.style.format("{:.3f}"),
                    use_container_width=True
                )

            # Botón de descarga
            csv_bytes = df_filtrado.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Descargar datos filtrados como CSV",
                data=csv_bytes,
                file_name="datos_filtrados.csv",
                mime="text/csv"
            )
        else:
            st.error("⚠️ No hay registros con los filtros aplicados. Amplía los rangos.")

    # ════════════════════════════════════════════════════════
    # SECCIÓN 6 — CONCLUSIONES
    # ════════════════════════════════════════════════════════
    elif "6️⃣" in seccion:
        st.markdown('<div class="section-header"><h3>6️⃣ Conclusiones del Análisis</h3></div>',
                    unsafe_allow_html=True)

        col_l, col_r = st.columns([2, 1])

        with col_l:
            st.subheader("🔍 Hallazgos principales del análisis")
            st.markdown("""
            Esta aplicación realizó un análisis exploratorio completo del dataset de consumo
            eléctrico, abarcando las siguientes dimensiones:

            **1. Exploración inicial:**
            Se identificó la estructura del dataset, los tipos de variables, la presencia de
            valores nulos y las dimensiones generales del conjunto de datos.

            **2. Análisis estadístico:**
            Se calcularon medidas de tendencia central y dispersión para cada variable numérica,
            permitiendo identificar distribuciones y valores atípicos (outliers).

            **3. Visualización temporal:**
            Se graficó la evolución del consumo eléctrico en el tiempo, identificando patrones,
            picos de demanda y tendencias generales.

            **4. Correlaciones:**
            Se analizaron las relaciones entre variables, detectando cuáles presentan mayor
            interdependencia con el consumo eléctrico.

            **5. Segmentación interactiva:**
            Los filtros dinámicos permiten aislar subconjuntos específicos para análisis
            más focalizados según criterios de ingeniería.
            """)

            st.subheader("💡 Recomendaciones técnicas")
            st.info("""
            • Implementar modelos de predicción (regresión, series de tiempo) para anticipar
              picos de consumo y optimizar la distribución energética.

            • Integrar variables externas como temperatura ambiente, hora del día y día
              de la semana para enriquecer el análisis.

            • Establecer alertas automáticas cuando el consumo supere umbrales críticos.

            • Considerar análisis de eficiencia energética por zona o tipo de equipamiento.
            """)

        with col_r:
            st.subheader("📌 Resumen del proyecto")
            st.markdown(f"""
            <div class="metric-card">
                <b>📁 Dataset:</b> {df.shape[0]:,} registros<br>
                <b>📋 Variables:</b> {df.shape[1]} columnas<br>
                <b>🔢 Numéricas:</b> {len(numericas)}<br>
                <b>🏷️ Categóricas:</b> {len(categoricas)}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.success("**Área:** Ingeniería / Tecnología")
            st.success("**Tema:** Consumo Eléctrico")
            st.success("**Herramienta:** Streamlit + Python")

            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📚 Tecnologías usadas")
            tecnologias = {
                "Python": "3.10+",
                "Streamlit": "1.28+",
                "Pandas": "1.5+",
                "Plotly": "5.13+",
                "Seaborn": "0.12+",
                "Matplotlib": "3.6+"
            }
            for tech, ver in tecnologias.items():
                st.markdown(f"- **{tech}** v{ver}")

        st.markdown("---")
        st.caption("⚡ Proyecto Final — Ciencia de Datos | Desarrollado con Streamlit")
