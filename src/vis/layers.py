"""
vis/plotly_layers.py
Funções de desenho em Plotly — substitui layers.py para uso no Streamlit.
"""

import numpy as np
import plotly.graph_objects as go

from src.data_pipe.data_prep import get_frame

from vis.lines_layer import _lines_data
from vis.stretch_layer import _stretch_index, _defensive_line_data, DEFENSIVE_LINE_THRESHOLD
from vis.skeleton_layer import _skeleton_data
from vis.delaunay_layer import _delaunay_data
from vis.hull_layer import _hull_data
from vis.field_layer import field_shapes

from src.config.settings import COLORS, PITCH_LENGTH, PITCH_WIDTH
import streamlit as st

# ── Camadas de um frame ────────────────────────────────────────────────────────
@st.cache_data
def _frame_traces(frame_df, active_layers):
    """Retorna lista de dicts de dados para um go.Frame."""
    data = []
    formations = {}
    stretches = {}

    for team in ["home", "away"]:
        tdf = frame_df[frame_df["team"] == team].dropna(subset=["x","y"])
        pts = tdf[["x","y"]].values

        # skeleton
        sx, sy = _skeleton_data(pts) if active_layers["skeleton"] else ([], [])
        data.append(dict(x=sx, y=sy))

        # delaunay
        dx, dy = _delaunay_data(pts) if active_layers["delaunay"] else ([], [])
        data.append(dict(x=dx, y=dy))

        # hull line
        hlx, hly, hfx, hfy = _hull_data(pts) if active_layers["hull"] else ([], [], [], [])
        data.append(dict(x=hlx, y=hly))

        # hull fill
        data.append(dict(x=hfx, y=hfy))

        # tactical lines
        lx, ly, ltx, lty, formation = _lines_data(pts) if active_layers.get("lines", False) else ([], [], None, None, "")
        data.append(dict(x=lx, y=ly))
        data.append(dict(x=[], y=[], text=[]))
        formations[team] = formation

        # defensive stretch index
        stretch = _stretch_index(pts) if active_layers.get("stretch", False) else None
        stretches[team] = stretch

        # jogadores
        labels = [r["player_id"].split("_")[-1] for _, r in tdf.iterrows()]
        speeds = tdf["speed"].fillna(0).round(1).tolist() if "speed" in tdf.columns else [0]*len(tdf)
        hover  = [f"#{label} | {speed} m/s" for label, speed in zip(labels, speeds)]

        legend_bits = [team.capitalize()]
        if formations.get(team):
            legend_bits.append(f"Form {formations[team]}")
        if stretches.get(team) is not None:
            legend_bits.append(f"Stretch {stretches[team]:.2f}")
        data.append(dict(x=tdf["x"].tolist(), y=tdf["y"].tolist(),
                         text=labels, hovertext=hover,
                         name=" | ".join(legend_bits)))

       # linha da defesa
        dlx, dly = _defensive_line_data(pts) if active_layers.get("stretch", False) else ([], [])
        stretch_val = stretches.get(team)
        is_critical = stretch_val is not None and stretch_val > DEFENSIVE_LINE_THRESHOLD

        if is_critical:
            data.append(dict(x=[], y=[]))
            data.append(dict(x=dlx, y=dly))
        else:
            data.append(dict(x=dlx, y=dly))
            data.append(dict(x=[], y=[]))

    # bola
    row = frame_df.iloc[0]
    bx = float(row["ball_x"]) if not np.isnan(row["ball_x"]) else None
    by = float(row["ball_y"]) if not np.isnan(row["ball_y"]) else None
    data.append(dict(x=[bx], y=[by]))

    return data, stretches


# ── Figura base (traces vazios com estilo fixo) ───────────────────────────────

def _base_traces():
    traces = []
    for team in ["home", "away"]:
        traces.append(go.Scatter(x=[], y=[], mode="lines",
            line=dict(color=COLORS["skeleton"], width=1), opacity=0.5,
            showlegend=False, hoverinfo="skip", name=f"skel_{team}"))
        traces.append(go.Scatter(x=[], y=[], mode="lines",
            line=dict(color=COLORS["delaunay"], width=1), opacity=0.45,
            showlegend=False, hoverinfo="skip", name=f"del_{team}"))
        traces.append(go.Scatter(x=[], y=[], mode="lines",
            line=dict(color=COLORS[team], width=1.5, dash="dash"), opacity=0.4,
            showlegend=False, hoverinfo="skip", name=f"hull_{team}"))
        traces.append(go.Scatter(x=[], y=[], fill="toself",
            fillcolor=COLORS[team], opacity=0.07, mode="none",
            showlegend=False, hoverinfo="skip", name=f"hullf_{team}"))
        traces.append(go.Scatter(x=[], y=[], mode="lines",
            line=dict(color=COLORS[team], width=2.2, dash="dot"), opacity=0.8,
            showlegend=False, hoverinfo="skip", name=f"lines_{team}"))
        traces.append(go.Scatter(x=[], y=[], mode="text",
            textfont=dict(color=COLORS[team], size=16, family="Arial Black"),
            showlegend=False, hoverinfo="skip", name=f"lines_label_{team}"))
        # jogadores
        traces.append(go.Scatter(x=[], y=[], mode="markers+text",
            marker=dict(size=18, color=COLORS[team], line=dict(color="white", width=1.5)),
            textposition="middle center",
            textfont=dict(color="white", size=9, family="Arial Black"),
            hoverinfo="text", showlegend=True, name=team.capitalize()))
        # linha da defesa normal
        traces.append(go.Scatter(x=[], y=[], mode="lines",
            line=dict(color=COLORS["skeleton"], width=2),
            opacity=0.5, showlegend=False, hoverinfo="skip",
            name=f"defline_{team}"))
        # linha defensiva crítica
        traces.append(go.Scatter(x=[], y=[], mode="lines",
            line=dict(color="#FF3333", width=2),
            opacity=0.8, showlegend=False, hoverinfo="skip",
            name=f"defline_critical_{team}"))

    traces.append(go.Scatter(x=[], y=[], mode="markers",
        marker=dict(size=14, color=COLORS["ball"],
                    line=dict(color="black", width=1.2)),
        showlegend=False, hoverinfo="skip", name="ball"))

    return traces


# ── Animação completa ─────────────────────────────────────────────────────────

def build_animation(df, ids, active_layers, fps=25.0, speed=1.0) -> go.Figure:
    """
    Monta figura Plotly com animação nativa (go.Frame).
    Sem flash, sem rerun do Streamlit.
    """

    interval = int(1000 / (fps * speed))  # ms por frame

    frames = []
    slider_steps = []

    for i, fid in enumerate(ids):
        frame_df = get_frame(df, fid)
        if frame_df.empty:
            continue

        ts = frame_df.iloc[0]["timestamp"]
        data, stretches = _frame_traces(frame_df, active_layers)

        annotations = []
        if active_layers.get("stretch", False):
            home_val = stretches.get("home")
            away_val = stretches.get("away")
            if home_val is not None:
                annotations.append(dict(
                    x=10.0, y=-0.22,
                    xref="paper", yref="paper",
                    xanchor="left",
                    text=f"🏠 Home Stretch: <b>{home_val:.2f}</b>",
                    showarrow=False,
                    font=dict(color="white", size=12),
                    bgcolor="#222222",
                    bordercolor="#444444",
                    borderwidth=1,
                ))
        if away_val is not None:
            annotations.append(dict(
                x=0.0, y=-0.28,
                xref="paper", yref="paper",
                xanchor="left",
                text=f"✈️ Away Stretch: <b>{away_val:.2f}</b>",
                showarrow=False,
                font=dict(color="white", size=12),
                bgcolor="#222222",
                bordercolor="#444444",
                borderwidth=1,
            ))

        frames.append(go.Frame(
            data=[go.Scatter(x=d["x"], y=d["y"],
                             text=d.get("text"), hovertext=d.get("hovertext"),
                             textposition=d.get("textposition"),
                             name=d.get("name"))
                  for d in data],
            name=str(i),
            layout=go.Layout(
                title_text=f"Frame {fid}  |  {ts:.1f}s",
                annotations=annotations,
            ),
        ))

        slider_steps.append(dict(
            args=[[str(i)], dict(frame=dict(duration=interval, redraw=True),
                                 mode="immediate", transition=dict(duration=0))],
            label=str(fid),
            method="animate",
        ))

    fig = go.Figure(data=_base_traces(), frames=frames)

    # popula o primeiro frame
    if frames:
        for i, trace_data in enumerate(frames[0].data):
            fig.data[i].x = trace_data.x
            fig.data[i].y = trace_data.y
            if hasattr(trace_data, "text") and trace_data.text:
                fig.data[i].text = trace_data.text
            if hasattr(trace_data, "hovertext") and trace_data.hovertext:
                fig.data[i].hovertext = trace_data.hovertext
            if hasattr(trace_data, "textposition") and trace_data.textposition:
                fig.data[i].textposition = trace_data.textposition
            if hasattr(trace_data, "name") and trace_data.name:
                fig.data[i].name = trace_data.name

    fig.update_layout(
        title=dict(text="Frame —", font=dict(color="white", size=13), x=0.5),
        paper_bgcolor="#111111",
        plot_bgcolor="#2d5a27",
        shapes=field_shapes(),
        xaxis=dict(range=[-3, PITCH_LENGTH+3], showgrid=False,
                   zeroline=False, showticklabels=False),
        yaxis=dict(range=[-3, PITCH_WIDTH+3], showgrid=False,
                   zeroline=False, showticklabels=False,
                   scaleanchor="x", scaleratio=1),
        margin=dict(l=10, r=10, t=50, b=80),
        legend=dict(font=dict(color="white"), bgcolor="#222222",
                    bordercolor="#444444", borderwidth=1),
        height=620,
        updatemenus=[dict(
            type="buttons", showactive=False,
            y=-0.08, x=0.07, xanchor="right",
            buttons=[
                dict(label="▶  Play",
                     method="animate",
                     args=[None, dict(frame=dict(duration=interval, redraw=True),
                                      fromcurrent=True,
                                      transition=dict(duration=0))]),
                dict(label="⏸  Pause",
                     method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False),
                                        mode="immediate",
                                        transition=dict(duration=0))]),
            ],
        )],
        sliders=[dict(
            active=0,
            steps=slider_steps,
            x=0.1, y=-0.02,
            len=0.9,
            currentvalue=dict(prefix="Frame: ", font=dict(color="white")),
            font=dict(color="white"),
            bgcolor="#333333",
            bordercolor="#555555",
        )],
    )

    return fig


# ── Frame único (snapshot) ────────────────────────────────────────────────────

def build_frame_figure(frame_df, active_layers) -> go.Figure:
    data, _ = _frame_traces(frame_df, active_layers)  # ← desempacota tuple
    traces = _base_traces()
    for i, d in enumerate(data):
        traces[i].x = d["x"]
        traces[i].y = d["y"]
        if d.get("text"):
            traces[i].text = d["text"]
        if d.get("hovertext"):
            traces[i].hovertext = d["hovertext"]
        if d.get("textposition"):
            traces[i].textposition = d["textposition"]
        if d.get("name"):
            traces[i].name = d["name"]

    fid = frame_df.iloc[0]["frame_id"]
    ts  = frame_df.iloc[0]["timestamp"]

    fig = go.Figure(data=traces)
    fig.update_layout(
        title=dict(text=f"Frame {fid}  |  {ts:.1f}s",
                   font=dict(color="white", size=13), x=0.5),
        paper_bgcolor="#111111",
        plot_bgcolor="#2d5a27",
        shapes=field_shapes(),
        xaxis=dict(range=[-3, PITCH_LENGTH+3], showgrid=False,
                   zeroline=False, showticklabels=False),
        yaxis=dict(range=[-3, PITCH_WIDTH+3], showgrid=False,
                   zeroline=False, showticklabels=False,
                   scaleanchor="x", scaleratio=1),
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(font=dict(color="white"), bgcolor="#222222",
                    bordercolor="#444444", borderwidth=1),
        height=620,
    )
    return fig