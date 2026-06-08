"""
buttontactics/colors.py
Constantes visuais e de configuração do sistema.
"""

# ── Campo ─────────────────────────────────────────────────────────────────────

PITCH_LENGTH = 105.0   # metros (padrão FIFA)
PITCH_WIDTH  = 68.0

PITCH_KWARGS = dict(
    pitch_type="custom",
    pitch_length=PITCH_LENGTH,
    pitch_width=PITCH_WIDTH,
    pitch_color="#2d5a27",
    line_color="white",
    linewidth=1.2,
)

# ── Paleta ────────────────────────────────────────────────────────────────────

COLORS = {
    "home"     : "#378ADD",   # azul
    "away"     : "#D85A30",   # coral
    "ball"     : "#F5C400",   # amarelo
    "skeleton" : "#AAAAAA",   # esqueleto tático
    "delaunay" : "#7F77DD",   # Shape Graph
}

# ── Player ────────────────────────────────────────────────────────────────────

SPEEDS       = [0.25, 0.5, 1.0, 2.0, 4.0]   # multiplicadores de velocidade
BASE_INTERVAL = 100                           # ms entre frames na velocidade 1x