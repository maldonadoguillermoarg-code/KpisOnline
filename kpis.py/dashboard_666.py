# =============================================================================
# ROCKEFELLER KPI - MODERN ADMIN UI EDITION (LIGHT MODE)
# =============================================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os
from streamlit_echarts import st_echarts
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container

# ─── CONFIGURACIÓN DE PÁGINA ────────────────────────────────────────────────
st.set_page_config(
    page_title="Executive Admin Panel",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── MOTOR CSS (ESTILO LIGHT ADMIN PANEL) ──────────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@300;400;600;700&display=swap');

    /* Fondo general claro como en la imagen */
    .stApp {
        background-color: #f4f7fa;
        color: #2d3748;
        font-family: 'Public Sans', sans-serif;
    }

    /* Tarjetas blancas con sombra suave */
    .chart-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }

    /* Sidebar con color sólido */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Títulos de sección */
    h3 {
        color: #4a5568;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# ─── PALETA DE COLORES (Según la imagen: Cian, Azul, Rosa) ──────────────────
UI_COLORS = ['#00b4d8', '#0077b6', '#ff4d6d', '#ff758f', '#90e0ef']

# ─── CARGA DE DATOS ─────────────────────────────────────────────────────────
@st.cache_data
def load_data_engine():
    path = "base_para_dashboard.parquet"
    if os.path.exists(path):
        try:
            df = pd.read_parquet(path)
            time_col = next((c for c in df.columns if any(x in c.lower() for x in ['time', 'fecha', 'date'])), None)
            if time_col: df = df.rename(columns={time_col: 'Timestamp'})
            else: df['Timestamp'] = pd.date_range(start='2025-01-01', periods=len(df), freq='H')
            if 'UX_Score' not in df.columns: df['UX_Score'] = np.random.uniform(7.0, 9.8, len(df))
            if 'Revenue_USD' not in df.columns: df['Revenue_USD'] = np.random.uniform(1000, 5000, len(df))
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            return df
        except: pass
    
    # Fallback
    return pd.DataFrame({
        'Timestamp': [datetime.now() - timedelta(hours=i) for i in range(100)],
        'Dimension_Internal': np.random.choice(['Tech', 'Fin', 'Ops'], 100),
        'Revenue_USD': np.random.uniform(5000, 20000, 100),
        'UX_Score': np.random.uniform(6.0, 9.9, 100)
    })

df = load_data_engine()

# ─── FILTROS SIDEBAR ────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50) # Icono de perfil
    st.title("Admin Panel")
    cat_col = next((c for c in df.columns if df[c].dtype == 'object'), df.columns[1])
    selected_cats = st.multiselect("Categorías", df[cat_col].unique(), default=df[cat_col].unique())
    df_f = df[df[cat_col].isin(selected_cats)].copy()

# ─── BLOQUE DE KPIs (Estilo limpio) ────────────────────────────────────────
st.subheader("Key Performance Indicators")
k1, k2, k3, k4 = st.columns(4)
with k1: st.metric("Revenue", f"${df_f['Revenue_USD'].sum()/1e3:.1f}k", "+2.5%")
with k2: st.metric("UX Score", f"{df_f['UX_Score'].mean():.2f}", "+0.4%")
with k3: st.metric("Efficiency", "94%", "Stable")
with k4: st.metric("Status", "Active", "Normal")

style_metric_cards(
    background_color="#ffffff",
    border_left_color="#00b4d8",
    border_color="#e2e8f0",
    box_shadow=False
)

# ─── LAYOUT DE GRÁFICOS (Estilo Adobe Stock) ───────────────────────────────
row1_col1, row1_col2 = st.columns([2, 1])

with row1_col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("Growth Analysis")
    # Gráfico de área suave con colores claros
    fig_area = px.area(df_f.sort_values('Timestamp'), x='Timestamp', y='Revenue_USD', 
                       color_discrete_sequence=[UI_COLORS[0]])
    fig_area.update_traces(fillcolor='rgba(0, 180, 216, 0.2)', line=dict(width=3))
    fig_area.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#4a5568"), height=300, margin=dict(l=0,r=0,t=0,b=0),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#edf2f7")
    )
    st.plotly_chart(fig_area, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("Distribution")
    # Donut chart como el de la imagen
    fig_pie = px.pie(df_f, names=cat_col, values='Revenue_USD', hole=0.7,
                     color_discrete_sequence=UI_COLORS)
    fig_pie.update_layout(showlegend=False, height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("Points Distribution")
    fig_scatter = px.scatter(df_f, x='Timestamp', y='UX_Score', color_discrete_sequence=[UI_COLORS[2]])
    fig_scatter.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("Multi-Category Bars")
    fig_bar = px.bar(df_f.head(10), y='Revenue_USD', color_discrete_sequence=[UI_COLORS[1]])
    fig_bar.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("Progress Monitor")
    # Gauge circular como en la imagen
    option = {
        "series": [{
            "type": 'gauge', "startAngle": 90, "endAngle": -270,
            "pointer": {"show": False}, "progress": {"show": True, "overlap": False, "roundCap": True, "clip": False},
            "axisLine": {"lineStyle": {"width": 15}},
            "splitLine": {"show": False}, "axisTick": {"show": False}, "axisLabel": {"show": False},
            "data": [{"value": 75, "itemStyle": {"color": UI_COLORS[0]}}],
            "detail": {"show": True, "formatter": '{value}%', "fontSize": 20, "color": '#2d3748', "offsetCenter": [0, 0]}
        }]
    }
    st_echarts(options=option, height="250px")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer limpio
st.markdown("<p style='text-align:center; color:#a0aec0; font-size:0.8rem;'>© 2026 Admin Analytics. All rights reserved.</p>", unsafe_allow_html=True)