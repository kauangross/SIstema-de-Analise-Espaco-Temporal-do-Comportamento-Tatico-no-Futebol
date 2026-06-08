"""
buttontactics/layers.py
Funções de desenho — cada função recebe um ax e dados, e plota uma camada.
Não sabe nada de slider, animação ou interação.
"""

import numpy as np
from matplotlib.collections import LineCollection
from mplsoccer import Pitch
from scipy.spatial import Delaunay, ConvexHull

from .colors import COLORS, PITCH_KWARGS


# ── Campo ─────────────────────────────────────────────────────────────────────

def draw_field(ax):
    """Desenha o campo no ax. Chamado a cada frame no modo interativo."""
    pitch = Pitch(**PITCH_KWARGS)
    pitch.draw(ax=ax)


# ── Jogadores ─────────────────────────────────────────────────────────────────

def draw_players(ax, frame_df):
    """Plota os círculos dos jogadores com o número do ID."""
    for team, color in [("home", COLORS["home"]), ("away", COLORS["away"])]:
        tdf = frame_df[frame_df["team"] == team]
        pts = tdf[["x", "y"]].dropna().values
        if len(pts) == 0:
            continue

        ax.scatter(pts[:, 0], pts[:, 1], s=220, c=color,
                   zorder=5, edgecolors="white", linewidths=1.5)

        for _, row in tdf.iterrows():
            pid = row["player_id"].split("_")[-1]
            ax.text(row["x"], row["y"], pid,
                    ha="center", va="center",
                    fontsize=7, fontweight="bold",
                    color="white", zorder=6)


# ── Bola ──────────────────────────────────────────────────────────────────────

def draw_ball(ax, frame_df):
    """Plota a bola."""
    bx, by = frame_df.iloc[0][["ball_x", "ball_y"]]
    if np.isnan(bx) or np.isnan(by):
        return
    ax.scatter(bx, by, s=140, c=COLORS["ball"], zorder=7,
               edgecolors="black", linewidths=1.2)


# ── Métricas ──────────────────────────────────────────────────────────────────

def draw_skeleton(ax, pts):
    """
    Esqueleto tático: conecta cada jogador aos 2 vizinhos mais próximos.
    pts: array (N, 2) com as coordenadas do time.
    """
    if len(pts) < 2:
        return
    segs = []
    for i, p in enumerate(pts):
        dists = np.linalg.norm(pts - p, axis=1)
        dists[i] = np.inf
        for j in np.argsort(dists)[:2]:
            segs.append([p, pts[j]])
    ax.add_collection(LineCollection(segs, colors=COLORS["skeleton"],
                                     linewidths=0.8, alpha=0.5, zorder=3))


def draw_delaunay(ax, pts):
    """
    Shape Graph: Triangulação de Delaunay sobre os jogadores do time.
    pts: array (N, 2) com as coordenadas do time.
    """
    if len(pts) < 3:
        return
    try:
        tri = Delaunay(pts)
        segs = []
        for simplex in tri.simplices:
            t = pts[simplex]
            for a, b in [(0, 1), (1, 2), (2, 0)]:
                segs.append([t[a], t[b]])
        ax.add_collection(LineCollection(segs, colors=COLORS["delaunay"],
                                         linewidths=0.9, alpha=0.45, zorder=4))
    except Exception:
        pass


def draw_hull(ax, pts, color):
    """
    Polígono convexo do time — representa o espaço ocupado.
    pts  : array (N, 2) com as coordenadas do time.
    color: cor do time (home ou away).
    """
    if len(pts) < 3:
        return
    try:
        hull = ConvexHull(pts)
        hp = np.append(hull.vertices, hull.vertices[0])
        ax.plot(pts[hp, 0], pts[hp, 1], color=color,
                linewidth=1.2, linestyle="--", alpha=0.4, zorder=3)
        ax.fill(pts[hull.vertices, 0], pts[hull.vertices, 1],
                color=color, alpha=0.06, zorder=2)
    except Exception:
        pass


# ── Frame completo ────────────────────────────────────────────────────────────

def draw_frame(ax, frame_df,
               show_skeleton: bool = True,
               show_delaunay: bool = True,
               show_hull: bool = True):
    """
    Orquestra todas as camadas de um frame.
    Espera um ax já limpo com o campo desenhado.
    """
    for team, color in [("home", COLORS["home"]), ("away", COLORS["away"])]:
        tdf = frame_df[frame_df["team"] == team]
        pts = tdf[["x", "y"]].dropna().values

        if show_skeleton:
            draw_skeleton(ax, pts)
        if show_delaunay:
            draw_delaunay(ax, pts)
        if show_hull:
            draw_hull(ax, pts, color)

    draw_players(ax, frame_df)
    draw_ball(ax, frame_df)