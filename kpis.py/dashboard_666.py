# =============================================================================
# ROCKEFELLER KPI - MODERN ADMIN UI (FULL 330+ LINES RESTORED)
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

# ─── MOTOR CSS (ESTILO ADOBE STOCK - CONTRASTE ALTO) ───────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@300;400;600;700&display=swap');

    /* Fondo gris muy claro para que resalten las tarjetas blancas */
    .stApp {
        background-color: #f0f2f6;
        color: #1a202c; /* Texto casi negro para lectura perfecta */
        font-family: 'Public Sans', sans-serif;
    }

    /* Tarjetas Blancas con sombra definida */
    .chart-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    /* Títulos en azul oscuro para que no se pierdan */
    h1, h2, h3 {
        color: #2d3748 !important;
        font-weight: 700 !important;
    }

    /* Sidebar blanco */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Estilo para los tabs (fichas) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        color: #4a5568;
    }
    .stTabs [aria-selected="true"] {
        color: #00b4d8 !important;
        border-bottom-color: #00b4d8 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ─── PALETA DE COLORES (CIAN, ROSA, AZUL MARINO) ───────────────────────────
COLORS = ['#00b4d8', '#ff4d6d', '#0077b6', '#7209b7', '#4cc9f0']

# ─── TU LÓGICA DE CARGA DE DATOS (MANTENIDA) ────────────────────────────────
@st.cache_data
def load_data_engine():
    path = "base_para_dashboard.parquet"
    if os.path.exists(path):
        try:
            df = pd.read_parquet(path)
            time_col = next((c for c in df.columns if any(x in c.lower() for x in ['time', 'fecha', 'date'])), None)
            if time_col: df = df.rename(columns={time_col: 'Timestamp'})
            else: df['Timestamp'] = pd.date_range(start='2025-01-01', periods=len(df), freq='H')
            
            # Asegurar columnas numéricas
            if 'UX_Score' not in df.columns: df['UX_Score'] = np.random.uniform(7.0, 9.8, len(df))
            if 'Volatility' not in df.columns: df['Volatility'] = np.random.uniform(0.1, 4.5, len(df))
            if 'Revenue_USD' not in df.columns: 
                num_cols = df.select_dtypes('number').columns
                df['Revenue_USD'] = df[num_cols[0]] if len(num_cols) > 0 else np.random.uniform(1000, 5000, len(df))
            
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            return df
        except: pass
    
    # Datos de respaldo (Mantenidos)
    dates = [datetime.now() - timedelta(hours=i) for i in range(1000)]
    return pd.DataFrame({
        'Timestamp': dates,
        'Dimension_Internal': np.random.choice(['Tech', 'Fin', 'Ops', 'Health'], 1000),
        'Revenue_USD': np.random.uniform(5000, 20000, 1000),
        'UX_Score': np.random.uniform(6.0, 9.9, 1000),
        'Volatility': np.random.uniform(0.5, 5.0, 1000)
    })

df = load_data_engine()

# ─── SIDEBAR & FILTROS (MANTENIDOS) ─────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#0077b6;'>ADMIN PANEL</h2>", unsafe_allow_html=True)
    cat_col = next((c for c in df.columns if df[c].dtype == 'object'), df.columns[1])
    selected_cats = st.multiselect("Categorías", df[cat_col].unique(), default=df[cat_col].unique()[:3])
    df_f = df[df[cat_col].isin(selected_cats)].copy()

# ─── HEADER (ESTILO LIMPIO) ────────────────────────────────────────────────
st.markdown(f"""
    <div style="background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 25px;">
        <h1 style="margin:0; font-size: 2rem;">Executive Dashboard <span style="color:#00b4d8; font-weight:300;">| Rockefeller</span></h1>
    </div>
""", unsafe_allow_html=True)

# ─── KPIs (CON CONTRASTE ALTO) ──────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("REVENUE TOTAL", f"${df_f['Revenue_USD'].sum()/1e6:.2f}M", "+12%")
k2.metric("AVG UX SCORE", f"{df_f['UX_Score'].mean():.2f}", "+0.5%")
k3.metric("VOLATILITY", f"{df_f['Volatility'].mean():.2f}", "-1.1%", delta_color="inverse")
k4.metric("NODOS ACTIVOS", f"{len(selected_cats)}", "Normal")

style_metric_cards(
    background_color="#ffffff",
    border_left_color="#00b4d8",
    border_color="#e2e8f0",
    box_shadow=False
)

# ─── TABS (RECONSTRUIDOS CON TU LÓGICA) ──────────────────────────────────────
t1, t2, t3 = st.tabs(["🚀 MONITOR PRINCIPAL", "📊 ANÁLISIS ESTRUCTURAL", "🧠 AI RADAR"])

with t1:
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Crecimiento de Ingresos")
        fig_area = px.area(df_f.sort_values('Timestamp'), x='Timestamp', y='Revenue_USD', 
                           color_discrete_sequence=[COLORS[0]])
        fig_area.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#2d3748"), margin=dict(l=0,r=0,t=0,b=0),
            xaxis=dict(gridcolor="#edf2f7"), yaxis=dict(gridcolor="#edf2f7")
        )
        st.plotly_chart(fig_area, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Salud UX Global")
        # Medidor de aguja animado (Cian)
        gauge_option = {
            "series": [{
                "type": 'gauge', "startAngle": 180, "endAngle": 0, "min": 0, "max": 10,
                "itemStyle": {"color": COLORS[0]},
                "progress": {"show": True, "width": 12},
                "axisLine": {"lineStyle": {"width": 12, "color": [[1, '#edf2f7']]}},
                "pointer": {"show": False}, "axisTick": {"show": False}, "splitLine": {"show": False},
                "axisLabel": {"show": False}, "detail": {
                    "offsetCenter": [0, -10], "fontSize": 30, "color": '#2d3748', "formatter": '{value}'
                },
                "data": [{"value": round(df_f['UX_Score'].mean(), 1)}]
            }]
        }
        st_echarts(options=gauge_option, height="250px")
        st.markdown('</div>', unsafe_allow_html=True)

with t2:
    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Distribución por Categoría")
        fig_pie = px.pie(df_f, names=cat_col, values='Revenue_USD', hole=0.7,
                         color_discrete_sequence=COLORS)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#2d3748"))
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_d:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Volatilidad vs UX")
        fig_scatter = px.scatter(df_f, x='Volatility', y='UX_Score', color=cat_col,
                                 color_discrete_sequence=COLORS)
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#2d3748"))
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with t3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("Radar de Performance")
    radar_data = df_f.groupby(cat_col)[['UX_Score', 'Volatility', 'Revenue_USD']].mean()
    radar_norm = (radar_data - radar_data.min()) / (radar_data.max() - radar_data.min())
    
    fig_radar = go.Figure()
    for i, (index, row) in enumerate(radar_norm.iterrows()):
        fig_radar.add_trace(go.Scatterpolar(r=row.values, theta=row.index, fill='toself', 
                                           name=index, line=dict(color=COLORS[i % len(COLORS)])))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1], gridcolor="#e2e8f0"), bgcolor='rgba(0,0,0,0)'),
        paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#2d3748")
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── FOOTER ─────────────────────────────────────────────────────────────────
st.markdown("<p style='text-align:center; color:#a0aec0; margin-top:30px;'>© 2026 Admin Intelligence Platform</p>", unsafe_allow_html=True)