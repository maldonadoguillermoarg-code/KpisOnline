import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuración de página
st.set_page_config(page_title="KPI Global Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Personalizado para diseño ultra moderno
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 15px; border-left: 5px solid #00d4ff; }
    .category-header { 
        background: linear-gradient(90deg, #00d4ff 0%, #004e92 100%);
        color: white; padding: 10px; border-radius: 10px; 
        text-align: center; margin-top: 30px; font-weight: bold; font-size: 24px;
    }
    .chart-container { background-color: #1e2130; padding: 10px; border-radius: 15px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Carga de datos optimizada
@st.cache_data
def load_data():
    # Asegúrate de que el nombre del archivo sea el correcto
    df = pd.read_csv("base_para_dashboard.csv", engine='pyarrow')
    return df

df = load_data()

# --- ENCABEZADO DE KPIs ---
st.title("🚀 Business Intelligence Portal")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Ventas Totales", f"$ {df['Venta'].sum():,.0f}", "+12%")
kpi2.metric("📦 Órdenes", f"{len(df):,}", "+5%")
kpi3.metric("👥 Clientes", "1,240", "Nuevos")
kpi4.metric("📈 ROI", "24.5%", "+2.1%")

st.markdown("---")

# --- FUNCIÓN PARA GENERAR BLOQUE DE 5 GRÁFICOS ---
def render_category_block(title, color_scale):
    st.markdown(f'<div class="category-header">{title}</div>', unsafe_allow_html=True)
    st.write("")
    
    # Disposición: 2 arriba, 1 al medio (grande), 2 abajo
    col_izq, col_med, col_der = st.columns([1, 2, 1])
    
    with col_izq:
        # Gráfico 1
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig1 = px.bar(df.head(5), x=df.columns[0], y='Venta', color_discrete_sequence=[color_scale[0]], title="Top Izquierda")
        fig1.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Gráfico 2
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig2 = px.line(df.head(10), y='Venta', title="Bottom Izquierda", color_discrete_sequence=[color_scale[1]])
        fig2.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_med:
        # Gráfico Central (Grande)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig3 = px.sunburst(df.head(100), path=[df.columns[0], df.columns[1]], values='Venta', color_continuous_scale=color_scale, title="Análisis Central")
        fig3.update_layout(height=540, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        # Gráfico 4
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig4 = px.area(df.head(10), y='Venta', title="Top Derecha", color_discrete_sequence=[color_scale[2]])
        fig4.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Gráfico 5
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig5 = px.pie(df.head(5), values='Venta', names=df.columns[0], hole=0.5, title="Bottom Derecha")
        fig5.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- RENDERIZADO DE LAS 3 CATEGORÍAS ---
render_category_block("📈 RENDIMIENTO FINANCIERO", ["#00d4ff", "#0083fe", "#004e92"])
render_category_block("🛒 MÉTRICAS DE OPERACIONES", ["#ff007a", "#ff4b2b", "#ac10fb"])
render_category_block("👥 ANÁLISIS DE CLIENTES", ["#00ff87", "#60efff", "#0061ff"])

st.markdown("---")
st.caption("Dashboard actualizado en tiempo real | v2.0")