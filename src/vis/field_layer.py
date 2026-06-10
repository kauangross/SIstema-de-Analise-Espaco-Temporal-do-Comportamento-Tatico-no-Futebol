from src.config.settings import PITCH_LENGTH, PITCH_WIDTH

# ── Campo ─────────────────────────────────────────────────────────────────────

def field_shapes():
    L, W = PITCH_LENGTH, PITCH_WIDTH
    return [
        dict(type="rect", x0=0, y0=0, x1=L, y1=W,
             line=dict(color="white", width=2)),
        dict(type="line", x0=L/2, y0=0, x1=L/2, y1=W,
             line=dict(color="white", width=1.5)),
        dict(type="circle", x0=L/2-9.15, y0=W/2-9.15,
             x1=L/2+9.15, y1=W/2+9.15,
             line=dict(color="white", width=1.5)),
        dict(type="circle", x0=L/2-0.5, y0=W/2-0.5,
             x1=L/2+0.5, y1=W/2+0.5,
             line=dict(color="white"), fillcolor="white"),
        dict(type="rect", x0=0, y0=W/2-20.15, x1=16.5, y1=W/2+20.15,
             line=dict(color="white", width=1.5)),
        dict(type="rect", x0=0, y0=W/2-9.16, x1=5.5, y1=W/2+9.16,
             line=dict(color="white", width=1.5)),
        dict(type="rect", x0=L-16.5, y0=W/2-20.15, x1=L, y1=W/2+20.15,
             line=dict(color="white", width=1.5)),
        dict(type="rect", x0=L-5.5, y0=W/2-9.16, x1=L, y1=W/2+9.16,
             line=dict(color="white", width=1.5)),
        dict(type="rect", x0=-2, y0=W/2-3.66, x1=0, y1=W/2+3.66,
             line=dict(color="white", width=1.5), fillcolor="#1a3a15"),
        dict(type="rect", x0=L, y0=W/2-3.66, x1=L+2, y1=W/2+3.66,
             line=dict(color="white", width=1.5), fillcolor="#1a3a15"),
    ]