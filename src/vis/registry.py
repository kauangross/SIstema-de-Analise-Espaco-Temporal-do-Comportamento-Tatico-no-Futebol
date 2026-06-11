from dataclasses import dataclass, field
from typing import Any, Callable

from src.config.settings import COLORS


@dataclass(frozen=True)
class TraceSpec:
    id: str
    per_team: bool = False
    style: dict[str, Any] = field(default_factory=dict)
    style_for_team: Callable[[str], dict[str, Any]] | None = None


@dataclass(frozen=True)
class LayerSpec:
    id: str
    label: str
    depends_on: tuple[str, ...] = ()
    traces: tuple[TraceSpec, ...] = ()


LAYERS = [
    LayerSpec(
        "skeleton",
        "Esqueleto tático",
        traces=(
            TraceSpec(
                id="skeleton",
                per_team=True,
                style={
                    "mode": "lines",
                    "line": {"color": COLORS["skeleton"], "width": 1},
                    "opacity": 0.5,
                    "showlegend": False,
                    "hoverinfo": "skip",
                },
            ),
        ),
    ),
    LayerSpec(
        "delaunay",
        "Shape Graph (Delaunay)",
        depends_on=("skeleton",),
        traces=(
            TraceSpec(
                id="delaunay",
                per_team=True,
                style={
                    "mode": "lines",
                    "line": {"color": COLORS["delaunay"], "width": 1},
                    "opacity": 0.45,
                    "showlegend": False,
                    "hoverinfo": "skip",
                },
            ),
        ),
    ),
    LayerSpec(
        "hull",
        "Polígono convexo",
        traces=(
            TraceSpec(
                id="hull_line",
                per_team=True,
                style_for_team=lambda team: {
                    "mode": "lines",
                    "line": {"color": COLORS[team], "width": 1.5, "dash": "dash"},
                    "opacity": 0.4,
                    "showlegend": False,
                    "hoverinfo": "skip",
                },
            ),
            TraceSpec(
                id="hull_fill",
                per_team=True,
                style_for_team=lambda team: {
                    "fill": "toself",
                    "fillcolor": COLORS[team],
                    "opacity": 0.07,
                    "mode": "none",
                    "showlegend": False,
                    "hoverinfo": "skip",
                },
            ),
        ),
    ),
    LayerSpec(
        "team_name",
        "Nome do time",
        traces=(
            TraceSpec(
                id="team_name",
                per_team=True,
                style_for_team=lambda team: {
                    "mode": "markers+text",
                    "marker": {
                        "size": 18,
                        "color": COLORS[team],
                        "line": {"color": "white", "width": 1.5},
                    },
                    "textposition": "middle center",
                    "textfont": {"color": "white", "size": 9, "family": "Arial Black"},
                    "hoverinfo": "text",
                    "showlegend": True,
                },
            ),
        ),
    ),
    LayerSpec(
        "ball",
        "Bola",
        traces=(
            TraceSpec(
                id="ball",
                style={
                    "mode": "markers",
                    "marker": {
                        "size": 14,
                        "color": COLORS["ball"],
                        "line": {"color": "black", "width": 1.2},
                    },
                    "showlegend": False,
                    "hoverinfo": "skip",
                },
            ),
        ),
    ),
]