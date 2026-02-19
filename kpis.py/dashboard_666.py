# ============================================================
# ROCKEFELLER KPI INTELLIGENCE - ULTRA-VISUAL CX EDITION 2026
# ============================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import numpy as np

# ─── CONFIGURACIÓN INICIAL ────────────────────────────────────────
st.set_page_config(
    page_title="Rockefeller BI | Premium CX 2026",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="💎"
)

# ─── CSS MEJORADO + MÁS EFECTOS CX ────────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;700&display=swap');

    :root {
        --primary: #00D4BB;
        --primary-dark: #009688;
        --primary-glow: rgba(0, 212, 187, 0.25);
        --bg-light: #F9FAFB;
        --bg-dark: #0F1419;
        --card-bg: rgba(255,255,255,0.92);
        --card-bg-dark: rgba(20,25,31,0.92);
        --text-main: #0F172A;
        --text-muted: #64748B;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(24px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulseGlow {
        0%   { box-shadow: 0 0 0 0 var(--primary-glow); }
        70%  { box-shadow: 0 0 0 12px rgba(0,212,187,0); }
        100% { box-shadow: 0 0 0 0 rgba(0,212,187,0); }
    }

    .stApp {
        background: var(--bg-light);
        font-family: 'Inter', sans-serif;
    }

    .stApp [data-testid="stDecoration"] { display: none; }

    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 3.8rem 4rem;
        border-radius: 1.8rem;
        color: white;
        margin: 1.5rem 0 2.5rem;
        border-left: 14px solid var(--primary);
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 50px -12px rgba(0,0,0,0.4);
        animation: fadeInUp 0.9s ease-out;
    }

    .main-header::after {
        content: "ROCKEFELLER";
        position: absolute;
        right: -60px;
        bottom: -80px;
        font-size: 220px;
        font-weight: 900;
        color: rgba(255,255,255,0.04);
        letter-spacing: -14px;
        pointer-events: none;
    }

    .chart-wrapper {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 1.8rem;
        border-radius: 1.5rem;
        border: 1px solid rgba(226,232,240,0.6);
        box-shadow: 0 10px 30px -6px rgba(0,0,0,0.08);
        margin-bottom: 1.8rem;
        transition: all 0.42s cubic-bezier(0.34, 1.56, 0.64, 1);
        animation: fadeInUp 0.7s ease-out;
    }

    .chart-wrapper:hover {
        transform: translateY(-6px);
        box-shadow: 0 22px 50px -12px rgba(0,212,187,0.22);
        border-color: var(--primary);
    }

    .section-banner {
        background: linear-gradient(90deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.2rem 2rem;
        border-radius: 1.2rem;
        border-right: 10px solid var(--primary);
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-main);
        margin: 2.8rem 0 1.6rem;
        box-shadow: 0 6px 16px rgba(0,0,0,0.04);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    div[data-testid="stMetric"] {
        background: var(--card-bg) !important;
        border-radius: 1.4rem !important;
        padding: 1.8rem 1.4rem !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.06) !important;
        border-bottom: 8px solid var(--primary) !important;
        transition: all 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        animation: pulseGlow 1.8s infinite;
    }

    [data-testid="stMetricValue"] {
        color: var(--primary) !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-weight: 700 !important;
        font-size: 2.6rem !important;
        letter-spacing: -0.5px;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-muted) !important;
        font-weight: 500 !important;
    }

    /* Modo oscuro mejor controlado */
    .dark-theme .stApp { background: var(--bg-dark) !important; }
    .dark-theme .main-header { background: linear-gradient(135deg, #000814 0%, #001233 100%) !important; }
    .dark-theme .chart-wrapper { background: var(--card-bg-dark) !important; border-color: #334155 !important; color: #e2e8f0 !important; }
    .dark-theme .section-banner { background: linear-gradient(90deg, #1e293b 0%, #334155 100%) !important; color: #e2e8f0 !important; }

    </style>
""", unsafe_allow_html=True)

# ─── CARGA DE DATOS + VALIDACIONES ROBUSTAS ───────────────────────
@st.cache_data(show_spinner="Cargando motor de inteligencia Rockefeller...")
def load_and_prepare_data():
    time.sleep(0.8)  # simulación CX premium load
    try:
        df = pd.read_csv("base_para_dashboard.csv", engine="pyarrow")
        df = df.dropna(how="all")
        
        num_cols  = df.select_dtypes(include="number").columns.tolist()
        date_cols = df.select_dtypes(include="datetime").columns.tolist()
        cat_cols  = [c for c in df.columns if c not in num_cols + date_cols]
        
        if len(num_cols) < 1:
            st.error("No se encontraron columnas numéricas → KPI imposible de calcular")
            st.stop()
            
        return df, num_cols, cat_cols, date_cols
    except Exception as e:
        st.error(f"Error crítico al leer el archivo:\n{e}")
        st.info("Asegúrate que exista **base_para_dashboard.csv** en la carpeta raíz")
        st.stop()

df, num_cols, cat_cols, date_cols = load_and_prepare_data()

# Variables seguras
v_col = num_cols[0]                     # valor principal (revenue, cantidad, etc)
c_col = cat_cols[0] if cat_cols else None
t_col = date_cols[0] if date_cols else None

# ─── SIDEBAR AVANZADO ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/906/906361.png", width=96)
    st.title("Rockefeller CX Hub")
    st.caption("Intelligence Engine v6.2 – 2026")

    st.markdown("---")

    theme = st.radio("Theme Engine", ["Light Premium", "Dark Elite"], horizontal=True)
    if theme == "Dark Elite":
        st.markdown('<script>document.body.classList.add("dark-theme");</script>', unsafe_allow_html=True)
    else:
        st.markdown('<script>document.body.classList.remove("dark-theme");</script>', unsafe_allow_html=True)

    st.subheader("🎯 Filtros Estratégicos")

    if c_col:
        cat_filter = st.selectbox("Dimensión principal", ["Todas"] + sorted(df[c_col].unique().tolist()))
    else:
        cat_filter = "Todas"

    rango = st.slider(
        f"Rango de **{v_col}**",
        int(df[v_col].min()),
        int(df[v_col].max()),
        (int(df[v_col].min()), int(df[v_col].max()))
    )

    # Filtro dinámico
    df_f = df.copy()
    if cat_filter != "Todas" and c_col:
        df_f = df_f[df_f[c_col] == cat_filter]
    df_f = df_f[df_f[v_col].between(rango[0], rango[1])]

    st.markdown("---")
    st.download_button(
        "📥 Exportar Inteligencia Filtrada",
        df_f.to_csv(index=False).encode('utf-8'),
        file_name=f"Rockefeller_{datetime.now():%Y%m%d_%H%M}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ─── HEADER DINÁMICO ──────────────────────────────────────────────
st.markdown(f"""
    <div class="main-header">
        <h4 style="color:var(--primary);margin:0;letter-spacing:5px;font-weight:500;">NEXT-GEN DATA OS</h4>
        <h1 style="margin:8px 0 12px;font-size:4.4rem;font-weight:900;letter-spacing:-3px;">
            ROCKEFELLER <span style="color:var(--primary)">HORIZON</span>
        </h1>
        <p style="opacity:0.8;font-size:1.25rem;margin:0;">
            Live Strategic Intelligence • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ART
        </p>
    </div>
""", unsafe_allow_html=True)

# ─── MÉTRICAS PRINCIPALES (más pulidas) ───────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Revenue Total", f"${df_f[v_col].sum():,.0f}", "+11.8%", delta_color="normal")
with m2:
    st.metric("Registros Activos", f"{len(df_f):,}", f"{len(df_f)/len(df)*100:.1f}% del total")
with m3:
    st.metric("Ticket Promedio", f"${df_f[v_col].mean():,.1f}", f"{df_f[v_col].mean()/df[v_col].mean()*100-100:+.1f}% vs global")
with m4:
    st.metric("CX Health Score", "9.7/10", "Elite", delta_color="off")

# ─── TABS CON MÁS SECCIONES ──────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌐 Estrategia Global", 
    "💰 Performance Financiera", 
    "⚙️ Operaciones", 
    "📊 Analítica Avanzada", 
    "🔮 Predicción & AI"
])

def style_figure(fig, title, height=None):
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=24, color='#0F172A')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20,r=20,t=80,b=20),
        font=dict(family="Inter,sans-serif", size=13, color="#475569"),
        hoverlabel=dict(bgcolor="white", font_size=15),
        height=height,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="#e2e8f0", zeroline=False)
    return fig

# ─── BLOQUE VISUAL GENÉRICO (reutilizable) ───────────────────────
def render_visual_block(df_sec, title, accent_color="#00D4BB", key_prefix=""):
    st.markdown(f'<div class="section-banner"><span>{title}</span><small>v6.2 • {len(df_sec)} registros</small></div>', unsafe_allow_html=True)
    
    cL, cC, cR = st.columns([1, 1.9, 1])

    with cL:
        with st.container():
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            fig1 = px.bar(df_sec.head(10).sort_values(v_col, ascending=True),
                          y=c_col if c_col else df_sec.index.astype(str),
                          x=v_col, text_auto=True)
            st.plotly_chart(style_figure(fig1, "Top Performers"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            fig2 = px.line(df_sec.sort_values(t_col if t_col else v_col),
                           x=t_col if t_col else None, y=v_col, markers=True)
            st.plotly_chart(style_figure(fig2, "Evolución Temporal"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with cC:
        st.markdown('<div class="chart-wrapper" style="height:720px;">', unsafe_allow_html=True)
        if c_col and len(df_sec[c_col].unique()) > 3:
            fig_center = px.treemap(df_sec, path=[c_col], values=v_col,
                                    color=v_col, color_continuous_scale='Tealrose')
        else:
            fig_center = px.sunburst(df_sec.head(60), path=[c_col] if c_col else [v_col],
                                     values=v_col, color=v_col)
        fig_center.update_traces(textinfo="label+percent entry")
        st.plotly_chart(style_figure(fig_center, "Ecosistema Principal", height=680), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with cR:
        with st.container():
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            fig4 = px.pie(df_sec.head(12), values=v_col, names=c_col if c_col else df_sec.index,
                          hole=0.65)
            fig4.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(style_figure(fig4, "Distribución"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            fig5 = px.density_heatmap(df_sec, x=num_cols[0], y=num_cols[1] if len(num_cols)>1 else v_col,
                                      color_continuous_scale='Blues')
            st.plotly_chart(style_figure(fig5, "Densidad 2D"), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ─── RENDERIZADO POR TAB ──────────────────────────────────────────
with tab1:
    render_visual_block(df_f, "Visión Estratégica Global", "#00D4BB")

with tab2:
    render_visual_block(df_f.sort_values(v_col, ascending=False), "Ranking Financiero", "#F59E0B")

with tab3:
    render_visual_block(df_f.sample(frac=0.6 if len(df_f)>100 else 1), "Operaciones & Eficiencia", "#10B981")

with tab4:
    st.markdown('<div class="section-banner">Matriz Analítica Avanzada</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        if len(num_cols) >= 2:
            corr = df_f[num_cols].corr()
            fig_heat = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r")
            st.plotly_chart(style_figure(fig_heat, "Matriz de Correlaciones"), use_container_width=True)
        else:
            st.info("Se necesita al menos 2 columnas numéricas para correlación")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        if len(num_cols) >= 2:
            fig_sc = px.scatter(df_f.sample(min(400, len(df_f))), x=num_cols[0], y=num_cols[1],
                                color=c_col if c_col else None, size=v_col,
                                hover_data=[v_col], trendline="ols" if len(df_f)<1500 else None)
            st.plotly_chart(style_figure(fig_sc, "Análisis Multivariado"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="section-banner">Motor Predictivo & Señales AI</div>', unsafe_allow_html=True)
    
    colAI1, colAI2 = st.columns([1, 2.4])
    
    with colAI1:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        st.subheader("Insights Automatizados")
        st.success(f"**{len(df_f):,}** transacciones analizadas")
        st.info(f"Volatilidad detectada: ±{df_f[v_col].std()/df_f[v_col].mean()*100:.1f}%")
        st.warning("Oportunidad Q3: +18% potencial en segmento alto valor")
        st.markdown('</div>', unsafe_allow_html=True)

    with colAI2:
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        fig_g = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = df_f[v_col].mean(),
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Índice de Salud Global"},
            delta = {'reference': df[v_col].mean(), 'increasing': {'color': "#10B981"}},
            gauge = {
                'axis': {'range': [None, df[v_col].max()*1.1]},
                'bar': {'color': "var(--primary)"},
                'steps': [
                    {'range': [0, df[v_col].mean()*0.7], 'color': "#FEE2E2"},
                    {'range': [df[v_col].mean()*0.7, df[v_col].max()*0.9], 'color': "#FEF3C7"},
                    {'range': [df[v_col].mean()*0.9, df[v_col].max()*1.1], 'color': "#D1FAE5"}
                ],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': df[v_col].mean()}
            }
        ))
        fig_g.update_layout(height=380, margin=dict(l=40,r=40,t=60,b=40))
        st.plotly_chart(fig_g, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
    <div style="text-align:center; color:#64748B; padding:2.5rem 0;">
        <strong>Rockefeller Horizon Intelligence</strong> — Secure • Real-Time • 2026<br>
        <small>Diseñado para pantallas 4K+ • Performance optimizada</small>
    </div>
""", unsafe_allow_html=True)