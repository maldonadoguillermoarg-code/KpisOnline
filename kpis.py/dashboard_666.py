# ============================================================
# ROCKEFELLER KPI INTELLIGENCE - ULTRA-VISUAL EDITION 2026
# ============================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Rockefeller BI | Premium", layout="wide", initial_sidebar_state="expanded")

# 2. INYECCIÓN DE CSS "INFINITO" (Estilo Apple / Bloomberg)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;800&family=IBM+Plex+Mono&display=swap');
    
    :root {
        --primary: #00B5AD;
        --secondary: #00827f;
        --bg-light: #F8F9FB;
        --card-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }

    /* Fondo y Contenedor */
    .stApp { background-color: var(--bg-light); }
    
    /* Header Premium */
    .main-header {
        background: linear-gradient(135deg, #1A1A1B 0%, #353535 100%);
        padding: 50px;
        border-radius: 30px;
        color: white;
        text-align: left;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
        border-bottom: 6px solid var(--primary);
    }
    
    .main-header::after {
        content: "BI";
        position: absolute;
        right: -20px;
        bottom: -20px;
        font-size: 200px;
        font-weight: 900;
        color: rgba(255,255,255,0.05);
    }

    /* Cards de Gráficos */
    .chart-wrapper {
        background: white;
        padding: 25px;
        border-radius: 24px;
        box-shadow: var(--card-shadow);
        border: 1px solid #EFEFEF;
        margin-bottom: 25px;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    }
    
    .chart-wrapper:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }

    /* Categorías */
    .section-banner {
        background: white;
        padding: 15px 30px;
        border-radius: 15px;
        border-left: 10px solid var(--primary);
        font-size: 26px;
        font-weight: 800;
        color: #1A1A1A;
        margin: 50px 0 30px 0;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.02);
    }

    /* Métricas */
    div[data-testid="stMetric"] {
        background: white !important;
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: var(--card-shadow) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: var(--primary) !important;
        font-family: 'IBM Plex Mono', monospace !important;
    }

    /* Tabs Personalizados */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 10px 10px 0 0;
        padding: 10px 25px;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE DATOS
@st.cache_data
def load_and_clean():
    df = pd.read_csv("base_para_dashboard.csv", engine="pyarrow")
    return df.dropna()

try:
    df = load_and_clean()
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    v_col = num_cols[0]; c_col = cat_cols[0]

    # 4. HEADER
    st.markdown(f"""
        <div class="main-header">
            <h4 style='color: var(--primary); margin:0;'>PREMIUM INTELLIGENCE</h4>
            <h1 style='margin:0; font-size: 55px; letter-spacing: -2px;'>ROCKEFELLER SYSTEMS</h1>
            <p style='opacity: 0.7;'>Global Data Analysis v4.0 | {datetime.now().strftime('%Y')}</p>
        </div>
    """, unsafe_allow_html=True)

    # 5. KPIs
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("REVENUE GEN", f"$ {df[v_col].sum():,.0f}", "↑ 12%")
    m2.metric("OPS VOLUME", f"{len(df):,}", "↑ 5.4%")
    m3.metric("UNIT MARGIN", f"$ {df[v_col].mean():,.2f}", "↓ 0.8%")
    m4.metric("EFFICIENCY", "94.2%", "Optimal")

    # 6. MOTOR DE ESTILO PLOTLY (INFOGRAFÍA)
    def make_pro_plot(fig, title, color="#00B5AD"):
        fig.update_layout(
            title=dict(text=f"<b>{title}</b>", font=dict(size=18, color="#333")),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=50, b=10),
            colorway=[color, "#FF851B", "#2ECC40", "#FF4136", "#B10DC9"]
        )
        fig.update_xaxes(showgrid=False, linecolor="#EEE")
        fig.update_yaxes(showgrid=True, gridcolor="#F0F0F0")
        return fig

    # 7. TABS CON DISEÑO "4 LADOS + 1 CENTRO"
    tabs = st.tabs(["💎 OVERVIEW", "💰 FINANCE", "📦 LOGISTICS"])

    def render_infographic_block(section_df, title, main_color):
        st.markdown(f'<div class="section-banner">{title}</div>', unsafe_allow_html=True)
        
        # Grid: [Lado, Lado, CENTRO, Lado, Lado] -> Simplificado en Streamlit a [1, 2, 1]
        l, c, r = st.columns([1, 2, 1])
        
        with l:
            # Gráfico 1
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            f1 = px.bar(section_df.head(5), x=c_col, y=v_col)
            st.plotly_chart(make_pro_plot(f1, "Rank A", main_color), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            # Gráfico 2
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            f2 = px.line(section_df.head(10), y=v_col)
            st.plotly_chart(make_pro_plot(f2, "Trend B", main_color), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c:
            # Gráfico Central (EL GIGANTE)
            st.markdown('<div class="chart-wrapper" style="height: 100%;">', unsafe_allow_html=True)
            f_mid = px.sunburst(section_df.head(50), path=[c_col, section_df.columns[1]], values=v_col)
            f_mid.update_layout(height=580)
            st.plotly_chart(make_pro_plot(f_mid, "CORE STRATEGY DISTRIBUTION", main_color), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with r:
            # Gráfico 4
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            f4 = px.pie(section_df.head(5), values=v_col, names=c_col, hole=0.6)
            st.plotly_chart(make_pro_plot(f4, "Ratio C", main_color), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            # Gráfico 5
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            f5 = px.area(section_df.head(8), y=v_col)
            st.plotly_chart(make_pro_plot(f5, "Growth D", main_color), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[0]:
        render_infographic_block(df, "EXECUTIVE SUMMARY", "#00B5AD")
    
    with tabs[1]:
        render_infographic_block(df.iloc[::-1], "FINANCIAL REVENUE", "#FF851B")
        
    with tabs[2]:
        render_infographic_block(df.sample(frac=0.5), "OPERATIONAL FLOW", "#2ECC40")

except Exception as e:
    st.error(f"SYSTEM CRITICAL ERROR: {e}")