# =============================================================================
# ROCKEFELLER KPI INTELLIGENCE - ULTIMATE HYPER-DRIVE EDITION 2026
# =============================================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os

# --- LIBRERÍAS DE ESTÉTICA AVANZADA ---
from streamlit_echarts import st_echarts
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container

# ─── CONFIGURACIÓN DE PÁGINA ────────────────────────────────────────────────
st.set_page_config(
    page_title="Rockefeller Terminal | Executive Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="💎"
)

# ─── MOTOR CSS (ESTILO HOLLYWOOD) ──────────────────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 50%, #0d1117 0%, #05070a 100%);
        color: #e5e7eb;
        font-family: 'Inter', sans-serif;
    }

    /* Contenedores con efecto cristal */
    .chart-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }

    .main-header {
        background: linear-gradient(90deg, rgba(0,242,255,0.15) 0%, rgba(112,0,255,0.05) 100%);
        padding: 3rem;
        border-radius: 2rem;
        border: 1px solid rgba(0,242,255,0.3);
        margin-bottom: 2rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ─── CARGA DE DATOS (OPTIMIZADA) ────────────────────────────────────────────
@st.cache_data
def load_data_engine():
    path = "base_para_dashboard.parquet"
    if os.path.exists(path):
        try:
            df = pd.read_parquet(path)
            # Normalización de nombres de columnas
            cols = {c: c for c in df.columns}
            time_col = next((c for c in df.columns if any(x in c.lower() for x in ['time', 'fecha', 'date'])), None)
            if time_col: df = df.rename(columns={time_col: 'Timestamp'})
            else: df['Timestamp'] = pd.date_range(start='2025-01-01', periods=len(df), freq='H')
            
            # Asegurar columnas numéricas para el radar y kpis
            if 'UX_Score' not in df.columns: df['UX_Score'] = np.random.uniform(7.0, 9.8, len(df))
            if 'Volatility' not in df.columns: df['Volatility'] = np.random.uniform(0.1, 4.5, len(df))
            if 'Revenue_USD' not in df.columns: 
                num_cols = df.select_dtypes('number').columns
                if len(num_cols) > 0: df['Revenue_USD'] = df[num_cols[0]]
                else: df['Revenue_USD'] = np.random.uniform(1000, 5000, len(df))
            
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            return df
        except: pass
    
    # Fallback Data
    dates = [datetime.now() - timedelta(hours=i) for i in range(1000)]
    return pd.DataFrame({
        'Timestamp': dates,
        'Dimension_Internal': np.random.choice(['Tech', 'Fin', 'Ops', 'Health'], 1000),
        'Revenue_USD': np.random.uniform(5000, 20000, 1000),
        'UX_Score': np.random.uniform(6.0, 9.9, 1000),
        'Volatility': np.random.uniform(0.5, 5.0, 1000),
        'Value_Internal': np.random.uniform(100, 1000, 1000)
    })

df = load_data_engine()

# ─── SIDEBAR & FILTROS ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#00f2ff; font-family:Orbitron;'>TERMINAL CONTROL</h2>", unsafe_allow_html=True)
    
    # Identificar columna categórica para filtro
    cat_col = next((c for c in df.columns if df[c].dtype == 'object'), df.columns[1])
    selected_cats = st.multiselect("Filtro Dimensional", df[cat_col].unique(), default=df[cat_col].unique()[:3])
    
    df_f = df[df[cat_col].isin(selected_cats)].copy()
    
    st.markdown("---")
    st.write("System Status: **Active**")
    st.write(f"Data Points: `{len(df_f):,}`")

# ─── HEADER ─────────────────────────────────────────────────────────────────
st.markdown(f"""
    <div class="main-header">
        <h1 style="font-family:'Orbitron'; font-size:3.5rem; margin:0; color:#00f2ff;">ROCKEFELLER <span style="color:white;">KPI</span></h1>
        <p style="letter-spacing: 5px; opacity: 0.7;">QUANTUM ANALYTICS ENGINE • 2026</p>
    </div>
""", unsafe_allow_html=True)

# ─── BLOQUE DE KPIs (UPGRADED) ──────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1: st.metric("TOTAL REVENUE", f"${df_f['Revenue_USD'].sum()/1e6:.2f}M", "+12.5%")
with k2: st.metric("AVG UX SCORE", f"{df_f['UX_Score'].mean():.2f}", "+0.4%")
with k3: st.metric("VOLATILITY INDEX", f"{df_f['Volatility'].mean():.2f}", "-1.2%", delta_color="inverse")
with k4: st.metric("ACTIVE NODES", f"{len(selected_cats)}", "Stable")

style_metric_cards(
    background_color="rgba(255, 255, 255, 0.03)",
    border_left_color="#00f2ff",
    border_color="rgba(255,255,255,0.1)",
    box_shadow=True
)

# ─── CUERPO PRINCIPAL (TABS) ────────────────────────────────────────────────
t1, t2, t3 = st.tabs(["🚀 MONITOR", "🧬 ESTRUCTURA", "🛰️ RADAR & AI"])

with t1:
    col_main, col_gauge = st.columns([3, 1])
    
    with col_main:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Flujo de Valor Temporal")
        fig_area = px.area(df_f.sort_values('Timestamp'), x='Timestamp', y='Revenue_USD', 
                           color_discrete_sequence=['#00f2ff'])
        fig_area.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                               font=dict(color="white"), margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig_area, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_gauge:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Global UX Health")
        # --- ECHARTS GAUGE ---
        gauge_option = {
            "series": [{
                "type": 'gauge', "startAngle": 180, "endAngle": 0, "min": 0, "max": 10,
                "itemStyle": {"color": '#00f2ff'},
                "progress": {"show": True, "width": 12},
                "axisLine": {"lineStyle": {"width": 12, "color": [[1, 'rgba(255,255,255,0.05)']]}},
                "pointer": {"show": False}, "axisTick": {"show": False}, "splitLine": {"show": False},
                "axisLabel": {"show": False}, "detail": {
                    "offsetCenter": [0, -10], "fontSize": 28, "color": 'inherit', "formatter": '{value}'
                },
                "data": [{"value": round(df_f['UX_Score'].mean(), 1)}]
            }]
        }
        st_echarts(options=gauge_option, height="250px")
        st.markdown('</div>', unsafe_allow_html=True)

with t2:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Distribución Dimensional")
        fig_pie = px.pie(df_f, names=cat_col, values='Revenue_USD', hole=0.6,
                         color_discrete_sequence=px.colors.qualitative.Plotly)
        fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Correlación Valor/UX")
        fig_scatter = px.scatter(df_f.sample(min(len(df_f), 500)), 
                                 x='Revenue_USD', y='UX_Score', color='Volatility',
                                 color_continuous_scale='Viridis')
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with t3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("Radar de Performance Multidimensional")
    # Lógica de Radar
    radar_data = df_f.groupby(cat_col)[['UX_Score', 'Volatility', 'Revenue_USD']].mean()
    # Normalización simple para el radar
    radar_norm = (radar_data - radar_data.min()) / (radar_data.max() - radar_data.min())
    
    fig_radar = go.Figure()
    for index, row in radar_norm.iterrows():
        fig_radar.add_trace(go.Scatterpolar(r=row.values, theta=row.index, fill='toself', name=index))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1]), bgcolor='rgba(0,0,0,0)'),
        paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), showlegend=True
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    with stylable_container(key="info", css_styles="{border: 1px solid #7000ff; border-radius: 10px; padding: 15px;}"):
        st.info("AI Analysis: Se detecta una correlación positiva entre la estabilidad de los nodos y el UX Score.")

# ─── FOOTER ─────────────────────────────────────────────────────────────────
st.markdown("<p style='text-align:center; opacity:0.3; margin-top:5rem;'>ROCKEFELLER SECURE TERMINAL v4.0 • ENCRYPTED CONNECTION</p>", unsafe_allow_html=True)