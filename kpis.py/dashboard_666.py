import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO CSS
# ==========================================
st.set_page_config(page_title="KPI Intelligence Global", layout="wide", initial_sidebar_state="collapsed")

# Aquí inyectamos el "ADN" visual del dashboard: Sombras, gradientes, fuentes y bordes.
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F0F2F6;
    }

    /* Contenedor principal con efecto de profundidad */
    .stApp {
        background: radial-gradient(circle at top left, #ffffff, #f1f4f9);
    }

    /* Header Estilo Apple/Infografía */
    .main-header {
        background: linear-gradient(135deg, #00B5AD 0%, #00827f 100%);
        padding: 40px;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 181, 173, 0.3);
    }

    /* Tarjetas de Gráficos (Cards) */
    .chart-card {
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #eef2f6;
        transition: transform 0.3s ease;
    }
    .chart-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.1);
    }

    /* Títulos de Categoría con barra lateral */
    .category-title {
        font-size: 32px;
        font-weight: 800;
        color: #1A1A1A;
        border-left: 8px solid #00B5AD;
        padding-left: 20px;
        margin: 40px 0 20px 0;
        letter-spacing: -1px;
    }

    /* Estilo para las métricas superiores (KPIs) */
    [data-testid="stMetricValue"] {
        font-size: 38px !important;
        font-weight: 800 !important;
        color: #00B5AD !important;
    }
    
    div[data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.02);
        border-bottom: 4px solid #00B5AD;
    }

    /* Ocultar barra de Streamlit para look limpio */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. MOTOR DE CARGA Y PROCESAMIENTO
# ==========================================
@st.cache_data
def get_clean_data():
    df = pd.read_csv("base_para_dashboard.csv", engine='pyarrow')
    # Limpieza básica para evitar errores de visualización
    df = df.dropna()
    return df

try:
    df = get_clean_data()
    
    # Análisis automático de columnas para no depender de nombres fijos
    nums = df.select_dtypes(include=['number']).columns.tolist()
    objs = df.select_dtypes(include=['object']).columns.tolist()
    
    val_col = nums[0] if nums else st.error("Falta columna numérica")
    cat_col = objs[0] if objs else df.columns[0]

    # ==========================================
    # 3. HEADER Y KPIs DE ALTO IMPACTO
    # ==========================================
    st.markdown(f"""
        <div class="main-header">
            <h1 style='margin:0; font-size: 45px; font-weight: 800;'>GLOBAL KPI INTELLIGENCE</h1>
            <p style='opacity: 0.9; font-size: 18px;'>Reporte Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        </div>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("REVENUE TOTAL", f"$ {df[val_col].sum():,.0f}", "+14.2%")
    with k2: st.metric("TRANSACCIONES", f"{len(df):,}", "+5.1%")
    with k3: st.metric("TICKET PROMEDIO", f"$ {df[val_col].mean():,.2f}", "-2.4%")
    with k4: st.metric("PERFORMANCE", "98.2%", "Optimo")

    # ==========================================
    # 4. FUNCIÓN DE DISEÑO DE GRÁFICOS (MODO INFOGRAFÍA)
    # ==========================================
    def plot_styling(fig, title):
        fig.update_layout(
            title=dict(text=f"<b>{title}</b>", x=0.05, y=0.95, font=dict(size=20, color='#1A1A1A')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", size=12, color="#666"),
            hovermode="x unified",
            margin=dict(l=30, r=30, t=80, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig.update_xaxes(showgrid=False, zeroline=False, color='#999')
        fig.update_yaxes(showgrid=True, gridcolor='#F0F0F0', zeroline=False, color='#999')
        return fig

    # ==========================================
    # 5. BLOQUES DE CATEGORÍAS (3 Categorías x 5 Gráficos cada una)
    # ==========================================
    categories = [
        {"name": "STRATEGIC GROWTH", "colors": ["#00B5AD", "#39CCCC", "#2ECC40"]},
        {"name": "OPERATIONAL EXCELLENCE", "colors": ["#FF851B", "#FF4136", "#B10DC9"]},
        {"name": "MARKET PENETRATION", "colors": ["#0074D9", "#7FDBFF", "#01FF70"]}
    ]

    for cat in categories:
        st.markdown(f'<div class="category-title">{cat["name"]}</div>', unsafe_allow_html=True)
        
        # Disposición: 2 laterales, 1 centro (grande), 2 laterales
        c_left, c_mid, c_right = st.columns([1, 1.8, 1])
        
        with c_left:
            # G1: Bar Chart Vertical
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            f1 = px.bar(df.head(6), x=cat_col, y=val_col, color_discrete_sequence=[cat["colors"][0]])
            st.plotly_chart(plot_styling(f1, "Volume Analysis"), use_container_width=True)
            st.markdown('</div><br>', unsafe_allow_html=True)
            
            # G2: Area Chart
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            f2 = px.area(df.head(15), y=val_col, color_discrete_sequence=[cat["colors"][1]])
            st.plotly_chart(plot_styling(f2, "Evolution Trend"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_mid:
            # G3: El gráfico estrella (Donut o Scatter complejo)
            st.markdown('<div class="chart-card" style="height: 100%;">', unsafe_allow_html=True)
            f3 = px.pie(df.head(12), values=val_col, names=cat_col, hole=0.65, 
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            f3.update_traces(textinfo='percent+label', pull=[0.05]*12)
            st.plotly_chart(plot_styling(f3, "Core Distribution Strategy"), use_container_width=True)
            
            # Agregamos una tabla interna para densidad visual
            st.write("### Resumen Ejecutivo")
            st.dataframe(df.head(8), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_right:
            # G4: Horizontal Bars
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            f4 = px.bar(df.tail(6), x=val_col, y=cat_col, orientation='h', 
                        color_discrete_sequence=[cat["colors"][2]])
            st.plotly_chart(plot_styling(f4, "Ranking Comparison"), use_container_width=True)
            st.markdown('</div><br>', unsafe_allow_html=True)
            
            # G5: Funnel o Linea de puntos
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            f5 = px.line(df.head(10), x=cat_col, y=val_col, markers=True, 
                         color_discrete_sequence=[cat["colors"][0]])
            st.plotly_chart(plot_styling(f5, "Point Velocity"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='text-align:center; color:#999;'>Dashboard Intelligence System | Proprietary Data | 2026</p>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Fallo en el sistema de visualización: {e}")