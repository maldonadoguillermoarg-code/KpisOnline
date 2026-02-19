import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="KPI Global Dashboard", layout="wide", initial_sidebar_state="collapsed")

# --- CSS MODERNO ---
st.markdown("""
    <style>
    /* Barra de navegación superior */
    .nav-bar {
        display: flex;
        justify-content: center;
        background: linear-gradient(90deg, #00d4ff 0%, #004e92 100%);
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 25px;
    }
    .nav-item {
        margin: 0 20px;
        font-weight: bold;
        color: white;
        cursor: pointer;
        font-size: 18px;
    }
    .nav-item:hover {
        text-decoration: underline;
    }
    /* KPIs estilo tarjetas */
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 15px;
        border-left: 5px solid #00d4ff;
    }
    .category-header { 
        background: linear-gradient(90deg, #00d4ff 0%, #004e92 100%);
        color: white; padding: 10px; border-radius: 10px; 
        text-align: center; margin-top: 30px; font-weight: bold; font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    return pd.read_csv("base_para_dashboard.csv", engine='pyarrow')

try:
    df = load_data()

    # Columnas detectadas
    cols_numericas = df.select_dtypes(include=['number']).columns.tolist()
    cols_texto = df.select_dtypes(include=['object']).columns.tolist()

    if not cols_numericas:
        st.error("No se encontraron columnas numéricas en el CSV.")
        st.stop()

    col_valor = cols_numericas[0]
    col_cat = cols_texto[0] if cols_texto else df.columns[0]

    # --- BARRA DE NAVEGACIÓN ---
    tabs = st.tabs(["🏠 Dashboard General", "📈 Rendimiento Financiero", "🛒 Métricas Operativas", "👥 Análisis por Categoría"])

    # --- TAB 1: DASHBOARD GENERAL ---
    with tabs[0]:
        st.title("🚀 Business Intelligence Portal")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric(f"💰 {col_valor} Total", f"$ {df[col_valor].sum():,.0f}")
        kpi2.metric("📦 Registros", f"{len(df):,}")
        kpi3.metric("📊 Columnas", f"{len(df.columns)}")
        kpi4.metric("📈 Max Valor", f"{df[col_valor].max():,.0f}")
        st.markdown("---")
        st.write("Selecciona una sección en la barra superior para explorar los gráficos.")

    # --- FUNCIÓN PARA BLOQUES DE GRÁFICOS ---
    def render_category_block(title, color_scale):
        st.markdown(f'<div class="category-header">{title}</div>', unsafe_allow_html=True)
        col_izq, col_med, col_der = st.columns([1, 2, 1])
        
        with col_izq:
            fig1 = px.bar(df.head(10), x=col_cat, y=col_valor, color_discrete_sequence=[color_scale[0]])
            fig1.update_layout(height=250, template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)

            fig2 = px.line(df.head(20), y=col_valor, color_discrete_sequence=[color_scale[1]])
            fig2.update_layout(height=250, template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

        with col_med:
            fig3 = px.histogram(df.head(100), x=col_cat, y=col_valor, color=col_cat, color_discrete_sequence=color_scale)
            fig3.update_layout(height=520, template="plotly_dark")
            st.plotly_chart(fig3, use_container_width=True)

        with col_der:
            fig4 = px.area(df.head(15), y=col_valor, color_discrete_sequence=[color_scale[2]])
            fig4.update_layout(height=250, template="plotly_dark")
            st.plotly_chart(fig4, use_container_width=True)

            fig5 = px.pie(df.head(10), values=col_valor, names=col_cat, hole=0.4)
            fig5.update_layout(height=250, template="plotly_dark")
            st.plotly_chart(fig5, use_container_width=True)

    # --- TAB 2: FINANCIERO ---
    with tabs[1]:
        render_category_block("📈 RENDIMIENTO FINANCIERO", ["#00d4ff", "#0083fe", "#004e92"])

    # --- TAB 3: OPERATIVO ---
    with tabs[2]:
        render_category_block("🛒 MÉTRICAS OPERATIVAS", ["#ff007a", "#ff4b2b", "#ac10fb"])

    # --- TAB 4: CATEGORÍAS ---
    with tabs[3]:
        render_category_block("👥 ANÁLISIS POR CATEGORÍA", ["#00ff87", "#60efff", "#0061ff"])

except Exception as e:
    st.error(f"Error crítico: {e}")
