"""
viz.py — ButtonTactics Pro
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from mplsoccer import Pitch
from scipy.spatial import Delaunay, ConvexHull

from data_pipe.data_prep import get_frame, frame_ids, PITCH_LENGTH, PITCH_WIDTH

def _draw_frame(ax, frame_df, show_skeleton, show_delaunay, show_hull):
    """Plota todos os elementos de um frame num ax limpo."""

    for team, color in [("home", COLORS["home"]), ("away", COLORS["away"])]:
        tdf = frame_df[frame_df["team"] == team]
        pts = tdf[["x", "y"]].dropna().values
        if len(pts) == 0:
            continue

        # jogadores
        ax.scatter(pts[:, 0], pts[:, 1], s=220, c=color,
                   zorder=5, edgecolors="white", linewidths=1.5)

        # labels
        for _, row in tdf.iterrows():
            pid = row["player_id"].split("_")[-1]
            ax.text(row["x"], row["y"], pid,
                    ha="center", va="center",
                    fontsize=7, fontweight="bold",
                    color="white", zorder=6)

        if len(pts) < 2:
            continue

        # esqueleto
        if show_skeleton:
            segs = []
            for i, p in enumerate(pts):
                dists = np.linalg.norm(pts - p, axis=1)
                dists[i] = np.inf
                for j in np.argsort(dists)[:2]:
                    segs.append([p, pts[j]])
            ax.add_collection(LineCollection(segs, colors=COLORS["skeleton"],
                                             linewidths=0.8, alpha=0.5, zorder=3))

        if len(pts) < 3:
            continue

        # delaunay
        if show_delaunay:
            try:
                tri = Delaunay(pts)
                segs = []
                for simplex in tri.simplices:
                    t = pts[simplex]
                    for a, b in [(0,1),(1,2),(2,0)]:
                        segs.append([t[a], t[b]])
                ax.add_collection(LineCollection(segs, colors=COLORS["delaunay"],
                                                 linewidths=0.9, alpha=0.45, zorder=4))
            except Exception:
                pass

        # convex hull
        if show_hull:
            try:
                hull = ConvexHull(pts)
                hp = np.append(hull.vertices, hull.vertices[0])
                ax.plot(pts[hp, 0], pts[hp, 1], color=color,
                        linewidth=1.2, linestyle="--", alpha=0.4, zorder=3)
                ax.fill(pts[hull.vertices, 0], pts[hull.vertices, 1],
                        color=color, alpha=0.06, zorder=2)
            except Exception:
                pass

    # bola
    bx, by = frame_df.iloc[0][["ball_x", "ball_y"]]
    if not (np.isnan(bx) or np.isnan(by)):
        ax.scatter(bx, by, s=140, c=COLORS["ball"], zorder=7,
                   edgecolors="black", linewidths=1.2)


def interactive(df, show_skeleton=True, show_delaunay=True, show_hull=True):

    ids = frame_ids(df)
    n   = len(ids)

    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor("#111111")
    fig.subplots_adjust(bottom=0.12)

    pitch = Pitch(**PITCH_KWARGS)

    ax_slider = fig.add_axes([0.15, 0.03, 0.70, 0.03])
    slider = widgets.Slider(
        ax_slider, "Frame",
        valmin=0, valmax=n - 1,
        valinit=0, valstep=1,
        color=COLORS["home"],
    )
    ax_slider.set_facecolor("#222222")
    slider.label.set_color("white")
    slider.valtext.set_color("white")

    def update(val):
        ax.cla()
        pitch.draw(ax=ax)  # redesenha campo

        fid      = ids[int(slider.val)]
        frame_df = get_frame(df, fid)
        if frame_df.empty:
            return

        _draw_frame(ax, frame_df, show_skeleton, show_delaunay, show_hull)

        ts = frame_df.iloc[0]["timestamp"]
        ax.set_title(f"Frame {fid}  |  {ts:.1f}s",
                     color="white", fontsize=11, pad=8)
        fig.canvas.draw_idle()

    slider.on_changed(update)
    update(0)
    plt.show()


def snapshot(df, frame_id, path="snapshot.png",
             show_skeleton=True, show_delaunay=True, show_hull=True):

    pitch = Pitch(**PITCH_KWARGS)
    fig, ax = pitch.draw(figsize=(14, 9))
    fig.patch.set_facecolor("#111111")

    frame_df = get_frame(df, frame_id)
    _draw_frame(ax, frame_df, show_skeleton, show_delaunay, show_hull)

    ts = frame_df.iloc[0]["timestamp"]
    ax.set_title(f"Frame {frame_id}  |  {ts:.1f}s",
                 color="white", fontsize=11, pad=8)

    fig.savefig(path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Salvo em {path}")