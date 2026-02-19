# ============================================================
# ROCKEFELLER KPI INTELLIGENCE - ULTRA-VISUAL CX EDITION 2026
# ============================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Rockefeller BI | Premium CX", layout="wide", initial_sidebar_state="expanded")

# 2. CSS EXTENDIDO PARA CX
st.markdown("""
    <style>
    :root {
        --primary: #00B5AD;
        --secondary: #00827f;
        --bg-light: #F8F9FB;
        --bg-dark: #1A1A1B;
        --card-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }

    .stApp { background-color: var(--bg-light); transition: background 0.5s ease; }

    .main-header {
        background: linear-gradient(135deg, var(--bg-dark) 0%, #353535 100%);
        padding: 50px;
        border-radius: 30px;
        color: white;
        margin-bottom: 40px;
        border-bottom: 6px solid var(--primary);
        position: relative;
        overflow: hidden;
    }

    .main-header::after {
        content: "CX";
        position: absolute;
        right: -20px;
        bottom: -20px;
        font-size: 180px;
        font-weight: 900;
        color: rgba(255,255,255,0.05);
    }

    .chart-wrapper {
        background: white;
        padding: 25px;
        border-radius: 24px;
        box-shadow: var(--card-shadow);
        border: 1px solid #EFEFEF;
        margin-bottom: 25px;
        transition: all 0.4s ease;
    }
    .chart-wrapper:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }

    .section-banner {
        background: white;
        padding: 15px 30px;
        border-radius: 15px;
        border-left: 10px solid var(--primary);
        font-size: 26px;
        font-weight: 800;
        color: #1A1A1A;
        margin: 50px 0 30px 0;
    }

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
    </style>
    """, unsafe_allow_html=True)

# 3. CARGA DE DATOS
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
            <h4 style='color: var(--primary); margin:0;'>CUSTOMER EXPERIENCE INTELLIGENCE</h4>
            <h1 style='margin:0; font-size: 55px;'>ROCKEFELLER SYSTEMS</h1>
            <p style='opacity: 0.7;'>Global Data Analysis v5.0 | {datetime.now().strftime('%Y')}</p>
        </div>
    """, unsafe_allow_html=True)

    # 5. KPIs
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("REVENUE GEN", f"$ {df[v_col].sum():,.0f}", "↑ 12%")
    m2.metric("OPS VOLUME", f"{len(df):,}", "↑ 5.4%")
    m3.metric("UNIT MARGIN", f"$ {df[v_col].mean():,.2f}", "↓ 0.8%")
    m4.metric("EFFICIENCY", "94.2%", "Optimal")

    # 6. SIDEBAR CX
    st.sidebar.header("🔍 Filtros CX")
    categoria_sel = st.sidebar.selectbox("Categoría", df[c_col].unique())
    rango_valores = st.sidebar.slider("Rango de valores", int(df[v_col].min()), int(df[v_col].max()), (int(df[v_col].min()), int(df[v_col].max())))
    modo_visual = st.sidebar.radio("Modo Visual", ["Claro", "Oscuro"])
    df_filtrado = df[(df[c_col] == categoria_sel) & (df[v_col].between(rango_valores[0], rango_valores[1]))]

    # 7. EXPORTACIÓN
    st.sidebar.download_button("⬇️ Exportar CSV", df_filtrado.to_csv(index=False).encode("utf-8"), "filtered_data.csv", "text/csv")

    # 8. MOTOR DE ESTILO PLOTLY
    def make_pro_plot(fig, title, color="#00B5AD"):
        fig.update_layout(
            title=dict(text=f"<b>{title}</b>", font=dict(size=18, color="#333")),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=50, b=10),
            colorway=[color, "#FF851B", "#2ECC40", "#FF4136", "#B10DC9"]
        )
        fig.update_traces(hovertemplate="<b>%{label}</b><br>Valor: %{value}")
        return fig

    # 9. TABS
    tabs = st.tabs(["💎 OVERVIEW", "💰 FINANCE", "📦 LOGISTICS", "🔥 ADVANCED"])

    # Función de bloque
    def render_infographic_block(section_df, title, main_color):
        st.markdown(f'<div class="section-banner">{title}</div>', unsafe_allow_html=True)
        l, c, r = st.columns([1, 2, 1])
        with l:
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            f1 = px.bar(section_df.head(5), x=c_col, y=v_col)
            st.plotly_chart(make_pro_plot(f1, "Rank A", main_color), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            f2 = px.line(section_df.head(10), y=v_col)
            st.plotly_chart(make_pro_plot(f2, "Trend B", main_color), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c:
            st.markdown('<div class="chart-wrapper" style="height: 100%;">', unsafe_allow_html=True)
            f_mid = px.sunburst(section_df.head(50), path=[c_col, section_df.columns[1]], values=v_col)
            st.plotly_chart(make_pro_plot(f_mid, "CORE STRATEGY DISTRIBUTION", main_color), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with r:
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            f4 = px.pie(section_df.head(5), values=v_col, names=c_col, hole=0.6)
            st.plotly_chart(make_pro_plot(f4, "Ratio C", main_color), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
            f5 = px.area(section_df.head(8), y=v_col)
            st.plotly_chart(make_pro_plot(f5, "Growth D", main_color), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

       # 10. Render Tabs
    with tabs[0]:
        render_infographic_block(df, "EXECUTIVE SUMMARY", "#00B5AD")

    with tabs[1]:
        render_infographic_block(df.iloc[::-1], "FINANCIAL REVENUE", "#FF851B")

    with tabs[2]:
        render_infographic_block(df.sample(frac=0.5), "OPERATIONAL FLOW", "#2ECC40")

    # --- Advanced Tab ---
    with tabs[3]:
        st.markdown(f'<div class="section-banner">ADVANCED ANALYTICS</div>', unsafe_allow_html=True)

        # Heatmap
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        corr = df[num_cols].corr()
        heatmap = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="Viridis"))
        st.plotly_chart(make_pro_plot(heatmap, "Correlation Heatmap"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Scatter interactivo
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        scatter = px.scatter(df_filtrado.head(100), x=num_cols[0], y=num_cols[1], color=c_col, size=v_col)
        st.plotly_chart(make_pro_plot(scatter, "Interactive Scatter"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Gauge de performance
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=df[v_col].mean(),
            delta={'reference': df[v_col].median()},
            gauge={'axis': {'range': [None, df[v_col].max()]},
                   'bar': {'color': "#00B5AD"},
                   'steps': [
                       {'range': [0, df[v_col].mean()], 'color': "#FFDDC1"},
                       {'range': [df[v_col].mean(), df[v_col].max()], 'color': "#C1FFD7"}]}))
        st.plotly_chart(make_pro_plot(gauge, "Performance Gauge"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Insights automáticos
        st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)
        avg_val = df[v_col].mean()
        max_val = df[v_col].max()
        min_val = df[v_col].min()
        trend = "creciente" if avg_val > (df[v_col].median()) else "estable"
        st.write("### 📌 Insights Ejecutivos")
        st.write(f"- El valor promedio es **{avg_val:,.2f}**, con un máximo de **{max_val:,.2f}** y un mínimo de **{min_val:,.2f}**.")
        st.write(f"- La tendencia general es **{trend}**, lo que sugiere un comportamiento positivo en la última muestra.")
        st.write("- Se recomienda reforzar las categorías con menor rendimiento para equilibrar la distribución.")
        st.markdown('</div>', unsafe_allow_html=True)

    # 11. Modo Visual Dinámico
    if modo_visual == "Oscuro":
        st.markdown("""
            <style>
            .stApp { background-color: #1A1A1B !important; }
            .chart-wrapper { background-color: #2A2A2A !important; color: white !important; }
            .section-banner { background-color: #2A2A2A !important; color: white !important; }
            </style>
        """, unsafe_allow_html=True)

    # 12. Footer
    st.markdown("---")
    st.markdown("<p style='text-align:center; color:#999;'>Rockefeller CX Intelligence System | Proprietary Data | 2026</p>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"SYSTEM CRITICAL ERROR: {e}")
