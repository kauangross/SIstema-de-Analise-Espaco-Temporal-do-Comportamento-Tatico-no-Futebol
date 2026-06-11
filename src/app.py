"""
app.py — ButtonTactics Pro
Interface Streamlit com animação nativa do Plotly (sem flash).

Rodar:
    streamlit run app.py
"""

import streamlit as st
from src.data_pipe.data_prep import prepare, frame_ids
from vis.layers import build_animation

# ── Configuração da página ────────────────────────────────────────────────────

st.set_page_config(
    page_title="ButtonTactics",
    page_icon="⚽",
    layout="wide",
)

st.markdown("""
    <style>
        body, .stApp { background-color: #111111; color: white; }
        .block-container { padding-top: 1rem; }
        label, .stCheckbox span { color: white !important; }
        h1, h2, h3 { color: white; }
    </style>
""", unsafe_allow_html=True)

LAYERS = {
    "skeleton": "Esqueleto tático",
    "delaunay": "Shape Graph (Delaunay)",
    "hull": "Polígono convexo",
    "lines": "Linhas de formação",
    "stretch": "Stretch defensivo",
}

# ── Cabeçalho ─────────────────────────────────────────────────────────────────

st.title("⚽ ButtonTactics")
st.caption("Análise Espaço-Temporal do Comportamento Tático no Futebol")

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("Configurações")

    match_id = st.selectbox("Partida", [1, 2, 3], index=0)
    limit    = st.number_input("Limite de frames (0 = todos)",
                               min_value=0, value=500, step=100)

    st.divider()
    st.subheader("Camadas")

    active_layers = {k: st.checkbox(LAYERS[k], value=True) for k in LAYERS.keys()}

    st.divider()
    st.subheader("Velocidade")
    speed = st.select_slider(
        "Velocidade de reprodução",
        options=[0.25, 0.5, 1.0, 2.0, 4.0],
        value=1.0,
        format_func=lambda x: f"{x}x",
    )

    st.divider()
    load = st.button("▶  Carregar e gerar animação", use_container_width=True)

# ── Carregamento ──────────────────────────────────────────────────────────────

@st.cache_data(show_spinner="Carregando dados…")
def load_data(match_id, limit):
    lim = limit if limit > 0 else None
    return prepare(match_id=match_id, limit=lim)

if "df" not in st.session_state or load:
    #with st.spinner("Carregando dados…"):
    st.session_state.df  = load_data(match_id, limit)
    st.session_state.ids = frame_ids(st.session_state.df)

df  = st.session_state.df
ids = st.session_state.ids

if len(ids) == 0:
    st.warning("Nenhum frame carregado.")
    st.stop()

# ── Animação ──────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner="Gerando animação…")
def get_animation(match_id, limit, active_layers, speed):
    """Cache da figura — só regera se algum parâmetro mudar."""
    d   = load_data(match_id, limit)
    ids = frame_ids(d)
    return build_animation(d, ids,active_layers,speed=speed)

# with st.spinner("Gerando animação…"):
fig = get_animation(match_id, limit, active_layers, speed)

st.plotly_chart(fig, use_container_width=True,
                config={"displayModeBar": False})