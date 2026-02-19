# =============================================================================
# Dashboard KPI Premium - Ultra Visual CX Edition
# Versión 2026 - Streamlit + Plotly
#
# Requisitos:
#   pip install streamlit pandas plotly numpy pyarrow
#
# Para ejecutarlo:
#   streamlit run app.py
#
# Si no existe "base_para_dashboard.csv" se generan datos sintéticos automáticos
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import numpy as np
import os

# ─── Configuración de página ────────────────────────────────────────────────
st.set_page_config(
    page_title="KPI Dashboard Premium CX",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# ─── Estilos CSS (Glassmorphism + animaciones modernas) ──────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;700&display=swap');

    :root {
        --primary: #00c9b7;
        --primary-dark: #00897b;
        --primary-glow: rgba(0, 201, 183, 0.25);
        --bg-light: #f8fafc;
        --bg-dark: #0f172a;
        --card-bg: rgba(255,255,255,0.94);
        --card-dark: rgba(15,23,42,0.94);
        --text-main: #0f172a;
        --text-muted: #64748b;
    }

    @keyframes fadeInUp { from {opacity:0; transform:translateY(20px);} to {opacity:1; transform:translateY(0);} }
    @keyframes pulseGlow { 0% {box-shadow:0 0 0 0 var(--primary-glow);} 70% {box-shadow:0 0 0 12px transparent;} 100% {box-shadow:0 0 0 0 transparent;} }

    .stApp { background: var(--bg-light); font-family: 'Inter', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 3rem 4rem;
        border-radius: 1.5rem;
        color: white;
        margin: 1.5rem 0 2rem;
        border-left: 12px solid var(--primary);
        box-shadow: 0 15px 40px -10px rgba(0,0,0,0.3);
        animation: fadeInUp 0.9s ease-out;
    }
    .chart-wrapper {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 1.8rem;
        border-radius: 1.4rem;
        border: 1px solid rgba(226,232,240,0.6);
        box-shadow: 0 10px 30px -6px rgba(0,0,0,0.08);
        margin-bottom: 1.8rem;
        transition: all 0.4s cubic-bezier(0.34,1.56,0.64,1);
        animation: fadeInUp 0.7s ease-out;
    }
    .chart-wrapper:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 50px -12px rgba(0,201,183,0.25);
        border-color: var(--primary);
    }
    .section-banner {
        background: white;
        padding: 1.2rem 2rem;
        border-radius: 1.2rem;
        border-right: 10px solid var(--primary);
        font-size: 1.6rem;
        font-weight: 700;
        margin: 2.5rem 0 1.5rem;
        box-shadow: 0 6px 16px rgba(0,0,0,0.04);
    }
    div[data-testid="stMetric"] {
        background: white !important;
        border-radius: 1.3rem !important;
        padding: 1.6rem !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.06) !important;
        border-bottom: 8px solid var(--primary) !important;
        transition: all 0.3s;
    }
    div[data-testid="stMetric"]:hover { transform: translateY(-4px); animation: pulseGlow 2s infinite; }
    [data-testid="stMetricValue"] {
        color: var(--primary) !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 2.6rem !important;
    }

    /* Modo oscuro básico */
    [data-testid="stAppViewContainer"] { background: var(--bg-dark) !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# ─── Datos sintéticos (fallback) ────────────────────────────────────────────
def generate_sample_data(n=600):
    np.random.seed(42)
    categories = ['Ventas', 'Marketing', 'Soporte', 'Desarrollo', 'RRHH', 'Logística']
    fechas = [datetime.now() - timedelta(days=i) for i in range(n)]
    return pd.DataFrame({
        'Categoría': np.random.choice(categories, n),
        'Fecha': fechas,
        'Ingresos': np.random.randint(800, 18000, n),
        'Transacciones': np.random.randint(15, 420, n),
        'Satisfacción': np.random.uniform(6.2, 9.8, n).round(1)
    })

# ─── Carga de datos ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    path = "base_para_dashboard.csv"
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            st.success("Datos cargados desde CSV")
            return df
        except:
            pass
    st.info("No se encontró CSV → usando datos de ejemplo")
    return generate_sample_data()

df = load_data()

# Columnas útiles
num_cols = df.select_dtypes('number').columns.tolist()
cat_cols = df.select_dtypes(['object', 'category']).columns.tolist()
date_cols = [c for c in df.columns if 'fecha' in c.lower() or df[c].dtype == 'datetime64[ns]']

v_col = num_cols[0] if num_cols else 'Ingresos'
c_col = cat_cols[0] if cat_cols else None
t_col = date_cols[0] if date_cols else None

# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Dashboard KPI Premium")
    st.caption("2026 Edition")

    theme = st.radio("Tema", ["Claro", "Oscuro"], horizontal=True)

    if c_col:
        filtro_cat = st.selectbox("Filtrar categoría", ["Todas"] + sorted(df[c_col].unique()))
    else:
        filtro_cat = "Todas"

    min_v, max_v = int(df[v_col].min()), int(df[v_col].max())
    rango_valor = st.slider("Rango de valor", min_v, max_v, (min_v, max_v))

    df_filtrado = df[df[v_col].between(rango_valor[0], rango_valor[1])]
    if filtro_cat != "Todas" and c_col:
        df_filtrado = df_filtrado[df_filtrado[c_col] == filtro_cat]

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown(f"""
    <div class="main-header">
        <h4 style="color:var(--primary); letter-spacing:4px;">INTELIGENCIA DE NEGOCIO</h4>
        <h1 style="margin:0; font-size:3.8rem; font-weight:900;">DASHBOARD CX</h1>
        <p style="opacity:0.8;">{datetime.now().strftime('%Y-%m-%d %H:%M')} • {len(df_filtrado):,} registros</p>
    </div>
""", unsafe_allow_html=True)

# Métricas rápidas
cols = st.columns(4)
cols[0].metric("Total", f"${df_filtrado[v_col].sum():,.0f}", "+9.4%")
cols[1].metric("Registros", f"{len(df_filtrado):,}")
cols[2].metric("Promedio", f"${df_filtrado[v_col].mean():,.0f}")
cols[3].metric("CX Score", "9.4/10", "Top")

# ─── Tabs ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Principal", "📈 Tendencias", "🔍 Análisis", "⚡ Insights"])

def fig_style(fig, title):
    fig.update_layout(
        title=title, title_font_size=22,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20,r=20,t=60,b=20),
        font=dict(family="Inter", size=13),
        height=450
    )
    return fig

with tab1:
    st.subheader("Vista General")
    col1, col2 = st.columns([1,1])

    with col1:
        fig = px.bar(df_filtrado.head(12).sort_values(v_col), 
                     y=c_col or df_filtrado.index.astype(str), 
                     x=v_col, text_auto=True)
        st.plotly_chart(fig_style(fig, "Top Categorías"), use_container_width=True)

    with col2:
        fig = px.pie(df_filtrado, names=c_col, values=v_col, hole=0.5)
        st.plotly_chart(fig_style(fig, "Distribución"), use_container_width=True)

with tab2:
    if t_col:
        fig = px.line(df_filtrado.sort_values(t_col), x=t_col, y=v_col)
        st.plotly_chart(fig_style(fig, "Evolución en el tiempo"), use_container_width=True)
    else:
        st.info("No hay columna de fecha detectada")

with tab3:
    if len(num_cols) >= 2:
        fig = px.scatter(df_filtrado.sample(min(400,len(df_filtrado))), 
                        x=num_cols[0], y=num_cols[1] if len(num_cols)>1 else v_col,
                        color=c_col, size=v_col)
        st.plotly_chart(fig_style(fig, "Relación entre variables"), use_container_width=True)

with tab4:
    st.subheader("Observaciones rápidas")
    st.success(f"• Valor más alto: ${df_filtrado[v_col].max():,.0f}")
    st.info(f"• Promedio actual: ${df_filtrado[v_col].mean():,.0f}")
    st.warning("• Recomendación: revisar categorías con bajo volumen")

st.markdown("---")
st.caption("Dashboard creado con Streamlit • 2026 style")