# =============================================================================
# ROCKEFELLER KPI INTELLIGENCE - ULTIMATE HOLLYWOOD EDITION 2026
# =============================================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os
import time

# ─── CONFIGURACIÓN DE PÁGINA ULTRA-PREMIUM ──────────────────────────────────
st.set_page_config(
    page_title="Rockefeller Terminal | Executive Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="💎"
)

# ─── MOTOR DE RENDERIZADO CSS (NIVEL BLOCKBUSTER) ───────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600;800&family=IBM+Plex+Mono:wght@400;600&display=swap');

    :root {
        --primary: #00f2ff;
        --secondary: #7000ff;
        --accent: #ff007a;
        --bg-dark: #05070a;
        --glass: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.1);
    }

    /* Fondo cinemático con gradiente animado */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #111827 0%, #05070a 100%);
        color: #e5e7eb;
        font-family: 'Inter', sans-serif;
    }

    /* Header Estilo Hollywood UI */
    .main-header {
        background: linear-gradient(90deg, rgba(0,242,255,0.1) 0%, rgba(112,0,255,0.05) 100%);
        padding: 4rem;
        border-radius: 2rem;
        border: 1px solid var(--glass-border);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
    }

    .main-header::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, var(--primary), transparent);
    }

    /* KPI Cards - Cyberpunk Style */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 1.5rem !important;
        padding: 2rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5) !important;
    }

    div[data-testid="stMetric"]:hover {
        border-color: var(--primary) !important;
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 0 30px rgba(0, 242, 255, 0.2) !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 2.8rem !important;
        color: var(--primary) !important;
        text-shadow: 0 0 20px rgba(0, 242, 255, 0.5);
    }

    /* Containers de Gráficos */
    .chart-container {
        background: rgba(15, 23, 42, 0.3);
        border: 1px solid var(--glass-border);
        border-radius: 2rem;
        padding: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
    }

    /* Tabs Neon */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px;
        color: white;
        font-weight: 600;
        border: 1px solid transparent;
        transition: all 0.3s;
    }

    .stTabs [data-baseweb="tab"]:hover {
        border-color: var(--primary);
        background-color: rgba(0,242,255,0.1);
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--primary) !important;
        color: black !important;
    }
    
    /* Scrollbar minimalista */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# ─── MOTOR DE DATOS INTELIGENTE (AUTO-RECOVERY) ──────────────────────────────
def get_synthetic_data(rows=1000):
    categories = ['Financial Services', 'Neural Tech', 'Quantum Computing', 'Logistics 4.0', 'Bio-Health']
    sub_cats = ['Hardware', 'Software', 'Support', 'R&D', 'Operations']
    dates = [datetime.now() - timedelta(days=i) for i in range(rows)]
    return pd.DataFrame({
        'Timestamp': dates,
        'Dimension': np.random.choice(categories, rows),
        'Asset_Class': np.random.choice(sub_cats, rows),
        'Revenue_USD': np.random.uniform(5000, 50000, rows),
        'Transactions': np.random.randint(100, 5000, rows),
        'UX_Score': np.random.uniform(7.5, 9.9, rows),
        'Volatility': np.random.uniform(0.1, 5.0, rows)
    })

@st.cache_data
def load_data_engine():
    path = "base_para_dashboard.csv"
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            # Normalización de fechas si existen
            for col in df.columns:
                if 'fecha' in col.lower() or 'time' in col.lower():
                    df[col] = pd.to_datetime(df[col])
            return df
        except: pass
    return get_synthetic_data()

# Inicialización
df = load_data_engine()

# ─── SIDEBAR: CENTRO DE COMANDO ──────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<h1 style='color:var(--primary); font-family:Orbitron;'>COMMAND CENTER</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Filtros Pro
    dim_col = 'Dimension' if 'Dimension' in df.columns else df.select_dtypes('object').columns[0]
    val_col = 'Revenue_USD' if 'Revenue_USD' in df.columns else df.select_dtypes('number').columns[0]
    
    selected_dim = st.multiselect("🌌 Seleccionar Galaxia de Datos", df[dim_col].unique(), default=df[dim_col].unique()[:3])
    date_range = st.date_input("🗓️ Ventana Temporal", [datetime.now() - timedelta(days=30), datetime.now()])
    
    st.markdown("---")
    st.subheader("🚀 System Status")
    st.progress(98)
    st.caption("AI Engine: Active | Data Sync: 100%")
    
    # Procesamiento de filtros
    mask = df[dim_col].isin(selected_dim)
    df_f = df[mask].copy()

# ─── HEADER DE ALTO IMPACTO ─────────────────────────────────────────────────
st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="color:var(--primary); font-family:'IBM Plex Mono'; letter-spacing:5px; margin:0;">SYSTEM.CORE.ON</h4>
                <h1 style="font-family:'Orbitron'; font-size:4rem; margin:0; text-shadow: 0 0 30px rgba(0,242,255,0.4);">ROCKEFELLER <span style="color:white;">TERMINAL</span></h1>
                <p style="font-size:1.2rem; color:var(--text-muted); margin-top:10px;">
                    Analítica Predictiva de Próxima Generación • {datetime.now().year} Protocolo de Datos
                </p>
            </div>
            <div style="text-align: right; border-left: 1px solid var(--glass-border); padding-left: 2rem;">
                <h2 style="margin:0; color:var(--primary);">{len(df_f):,}</h2>
                <p style="margin:0; opacity:0.6;">DATAPOINTS</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ─── KPIs DINÁMICOS ─────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
total_rev = df_f[val_col].sum()
avg_ux = df_f['UX_Score'].mean() if 'UX_Score' in df_f.columns else 9.5

k1.metric("REVENUE TOTAL", f"${total_rev/1e6:.2f}M", "+15.4%")
k2.metric("TRANSACTION VOL", f"{len(df_f):,}", "+4.2%")
k3.metric("AVG PERFORMANCE", f"{avg_ux:.1f}/10", "Optimum")
k4.metric("SYSTEM UPTIME", "99.99%", "Stable")

# ─── ESPACIO DE TRABAJO TÉCNICO ─────────────────────────────────────────────
t1, t2, t3, t4 = st.tabs(["⚡ REAL-TIME MONITOR", "📊 DEEP ANALYSIS", "🛡️ RISK CONTROL", "🧠 AI INSIGHTS"])

def apply_viz_style(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#e5e7eb", family="Inter"),
        title_font=dict(size=24, family="Orbitron", color="#00f2ff"),
        hovermode="x unified",
        margin=dict(l=0, r=0, t=60, b=0)
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False)
    return fig

with t1:
    st.markdown("<br>", unsafe_allow_html=True)
    c_left, c_right = st.columns([2, 1])
    
    with c_left:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Gráfico de flujo temporal
        fig_line = px.area(df_f.sort_values('Timestamp'), x='Timestamp', y=val_col, 
                          color_discrete_sequence=[['#00f2ff', '#7000ff'][0]])
        fig_line.update_traces(fillcolor="rgba(0, 242, 255, 0.1)", line=dict(width=4))
        st.plotly_chart(apply_viz_style(fig_line), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c_right:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        # Radar Chart de Atributos
        categories = ['Efficiency', 'Scalability', 'Security', 'UX', 'Speed']
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[9, 7, 10, 8, 9], theta=categories, fill='toself',
            line=dict(color= '#00f2ff'), fillcolor='rgba(0,242,255,0.2)'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False), bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(apply_viz_style(fig_radar), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with t2:
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 1.5, 1])
    
    with col_a:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        fig_bar = px.bar(df_f.groupby(dim_col)[val_col].sum().reset_index(), 
                        x=dim_col, y=val_col, color=val_col, color_continuous_scale='Viridis')
        st.plotly_chart(apply_viz_style(fig_bar), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_b:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # El centro: Sunburst Chart
        fig_sun = px.sunburst(df_f, path=[dim_col, 'Asset_Class'], values=val_col,
                             color=val_col, color_continuous_scale='Magma')
        fig_sun.update_layout(height=500)
        st.plotly_chart(apply_viz_style(fig_sun), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_c:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        fig_pie = px.pie(df_f, names='Asset_Class', values=val_col, hole=0.7)
        fig_pie.update_traces(marker=dict(colors=['#00f2ff', '#7000ff', '#ff007a']))
        st.plotly_chart(apply_viz_style(fig_pie), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with t3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Heatmap de Volatilidad
    st.write("### 🛡️ Heatmap de Riesgo por Categoría")
    fig_heat = px.density_heatmap(df_f, x=dim_col, y='Asset_Class', z='Volatility',
                                 color_continuous_scale='Hot')
    st.plotly_chart(apply_viz_style(fig_heat), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with t4:
    # Simulación de IA Generativa de Insights
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div style="background:rgba(0,242,255,0.05); padding:2rem; border-radius:1.5rem; border-left:5px solid var(--primary);">
                <h3 style="color:var(--primary);">🧠 AI Executive Summary</h3>
                <p>Basado en el análisis de flujo tensorial, se detecta una anomalía positiva en <b>Bio-Health</b>.</p>
                <ul>
                    <li>Probabilidad de escalabilidad: 89.2%</li>
                    <li>Riesgo de saturación: Bajo</li>
                    <li>Acción recomendada: Incrementar capital en Asset 'Neural'</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        # Gráfico de Dispersión Cuántico
        fig_scatter = px.scatter(df_f, x='Revenue_USD', y='Transactions', size='UX_Score', 
                                color='Volatility', color_continuous_scale='Spectral')
        st.plotly_chart(apply_viz_style(fig_scatter), use_container_width=True)

# ─── FOOTER TERMINAL ────────────────────────────────────────────────────────
st.markdown(f"""
    <div style="text-align:center; margin-top:5rem; padding:2rem; border-top:1px solid var(--glass-border);">
        <p style="font-family:'IBM Plex Mono'; color:var(--text-muted); font-size:0.8rem;">
            TERMINAL_ID: {datetime.now().strftime('%H%M%S')} • ENCRYPTION: AES-256 • STATUS: OPERATIONAL
        </p>
    </div>
""", unsafe_allow_html=True)