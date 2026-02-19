import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de alto nivel
st.set_page_config(page_title="Executive Analytics 666", layout="wide")

# Estética Profesional (Personalización de colores)
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px; color: #00D4FF; }
    .main { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_ready_data():
    # Lee el archivo que subiste a GitHub
    df = pd.read_csv("base_para_dashboard.csv")
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'])
    return df

def main():
    st.title("📊 Business Intelligence Dashboard")
    st.caption("Analizando la base optimizada por Motor 666.py")

    try:
        df = load_ready_data()
    except Exception as e:
        st.error(f"Error: No se encontró 'base_para_dashboard.csv' en el repositorio. Asegúrate de subirlo junto al código.")
        return

    # --- FILTROS EN SIDEBAR ---
    st.sidebar.header("Panel de Control")
    
    # Filtro Temporal
    if 'fecha' in df.columns and not df['fecha'].isnull().all():
        min_f, max_f = df['fecha'].min().date(), df['fecha'].max().date()
        rango = st.sidebar.date_input("Rango de Análisis", [min_f, max_f])
        if len(rango) == 2:
            df = df[(df['fecha'].dt.date >= rango[0]) & (df['fecha'].dt.date <= rango[1])]

    # Filtro de Producto
    if 'producto' in df.columns:
        prod_sel = st.sidebar.multiselect("Filtrar Productos", options=df['producto'].unique())
        if prod_sel:
            df = df[df['producto'].isin(prod_sel)]

    # --- KPI STRATEGY (Los 15 KPIs en vista compacta) ---
    col1, col2, col3, col4 = st.columns(4)
    
    revenue = df['ventas'].sum()
    transacciones = len(df)
    ticket_prom = revenue / transacciones if transacciones > 0 else 0
    margen_total = df['margen_bruto'].sum() if 'margen_bruto' in df.columns else 0
    
    col1.metric("Revenue Total", f"${revenue:,.2f}")
    col2.metric("Volumen Ventas", f"{transacciones:,}")
    col3.metric("Ticket Promedio", f"${ticket_prom:,.2f}")
    col4.metric("Margen de Contribución", f"${margen_total:,.2f}")

    st.markdown("---")

    # --- VISUALIZACIÓN PROFUNDA ---
    fila_top = st.columns(2)

    with fila_top[0]:
        st.subheader("📈 Tendencia de Crecimiento")
        # Agrupamos por año_mes que ya viene del 666.py
        if 'año' in df.columns and 'mes' in df.columns:
            df['periodo'] = df['año'].astype(str) + "-" + df['mes'].astype(str).str.zfill(2)
            evol = df.groupby('periodo')['ventas'].sum().reset_index()
            fig_line = px.line(evol, x='periodo', y='ventas', markers=True, template="plotly_dark")
            fig_line.update_traces(line_color='#00D4FF')
            st.plotly_chart(fig_line, use_container_width=True)

    with fila_top[1]:
        st.subheader("🏆 Top 10 Productos")
        if 'producto' in df.columns:
            top_p = df.groupby('producto')['ventas'].sum().sort_values(ascending=False).head(10).reset_index()
            fig_bar = px.bar(top_p, x='ventas', y='producto', orientation='h', 
                             color='ventas', color_continuous_scale='Blues')
            st.plotly_chart(fig_bar, use_container_width=True)

    fila_bottom = st.columns(2)

    with fila_bottom[0]:
        st.subheader("📅 Ventas por Día de la Semana")
        if 'dia_nombre' in df.columns:
            orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dias = df.groupby('dia_nombre')['ventas'].sum().reindex(orden).reset_index()
            fig_radar = px.line_polar(dias, r='ventas', theta='dia_nombre', line_close=True)
            st.plotly_chart(fig_radar, use_container_width=True)

    with fila_bottom[1]:
        st.subheader("👥 Concentración de Clientes (Pareto)")
        if 'cliente_id' in df.columns:
            clientes = df.groupby('cliente_id')['ventas'].sum().sort_values(ascending=False).head(20).reset_index()
            fig_pie = px.pie(clientes, values='ventas', names='cliente_id', hole=0.5)
            st.plotly_chart(fig_pie, use_container_width=True)

    # Vista de tabla para inspección profunda
    with st.expander("Explorar Base de Datos Completa"):
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()