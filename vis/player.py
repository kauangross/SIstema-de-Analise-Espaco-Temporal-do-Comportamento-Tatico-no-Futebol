"""
buttontactics/player.py
...
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
from matplotlib.animation import FuncAnimation

from data_pipe.data_prep import get_frame, frame_ids
from .colors import COLORS, PITCH_KWARGS, SPEEDS, BASE_INTERVAL
from .layers import draw_field, draw_frame

_anim_ref = None


def interactive(df, show_skeleton=True, show_delaunay=True, show_hull=True):

    ids = frame_ids(df)
    n = len(ids)
    state = {"playing": False, "speed_idx": 2}  # começa em 1x

    # ── layout ──────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor("#111111")
    fig.subplots_adjust(bottom=0.18)

    # slider de frames
    ax_slider = fig.add_axes([0.15, 0.10, 0.70, 0.025])
    slider = widgets.Slider(
        ax_slider, "Frame",
        valmin=0, valmax=n - 1,
        valinit=0, valstep=1,
        color=COLORS["home"],
    )
    ax_slider.set_facecolor("#222222")
    slider.label.set_color("white")
    slider.valtext.set_color("white")

    # botão Play/Pause
    ax_play = fig.add_axes([0.43, 0.04, 0.08, 0.04])
    btn_play = widgets.Button(ax_play, "▶  Play",
                              color="#333355", hovercolor="#444477")
    btn_play.label.set_color("white")
    btn_play.label.set_fontsize(9)

    # botão velocidade −
    ax_slower = fig.add_axes([0.32, 0.04, 0.07, 0.04])
    btn_slower = widgets.Button(ax_slower, "◀  Slower",
                                color="#333333", hovercolor="#555555")
    btn_slower.label.set_color("white")
    btn_slower.label.set_fontsize(9)

    # botão velocidade +
    ax_faster = fig.add_axes([0.55, 0.04, 0.07, 0.04])
    btn_faster = widgets.Button(ax_faster, "Faster  ▶",
                                color="#333333", hovercolor="#555555")
    btn_faster.label.set_color("white")
    btn_faster.label.set_fontsize(9)

    # label de velocidade atual
    ax_speed_lbl = fig.add_axes([0.64, 0.04, 0.06, 0.04])
    ax_speed_lbl.set_axis_off()
    speed_text = ax_speed_lbl.text(
        0.5, 0.5, f"{SPEEDS[state['speed_idx']]}x",
        ha="center", va="center",
        color="white", fontsize=10, fontweight="bold",
        transform=ax_speed_lbl.transAxes
    )

    # ── renderização ────────────────────────────────────────────────────
    def render(idx):
        ax.cla()
        draw_field(ax)

        fid      = ids[idx]
        frame_df = get_frame(df, fid)
        if frame_df.empty:
            return

        draw_frame(ax, frame_df, show_skeleton, show_delaunay, show_hull)

        ts = frame_df.iloc[0]["timestamp"]
        ax.set_title(f"Frame {fid}  |  {ts:.1f}s",
                     color="white", fontsize=11, pad=8)
        fig.canvas.draw_idle()

    render(0)

    # ── animação ────────────────────────────────────────────────────────
    def get_interval():
        return int(BASE_INTERVAL / SPEEDS[state["speed_idx"]])

    def animate(_):
        if not state["playing"]:
            return
        new_val = int(slider.val) + 1
        if new_val >= n:
            new_val = 0   # loop
        slider.set_val(new_val)

    def start_anim():
        global _anim_ref
        if _anim_ref is not None:
            _anim_ref.event_source.stop()
        _anim_ref = FuncAnimation(
            fig, animate,
            interval=get_interval(),
            cache_frame_data=False,
        )

    # ── callbacks ───────────────────────────────────────────────────────
    def on_slider(val):
        render(int(val))

    def on_play(event):
        state["playing"] = not state["playing"]
        if state["playing"]:
            btn_play.label.set_text("⏸  Pause")
            start_anim()
        else:
            btn_play.label.set_text("▶  Play")
            if _anim_ref:
                _anim_ref.event_source.stop()
        fig.canvas.draw_idle()

    def on_slower(event):
        if state["speed_idx"] > 0:
            state["speed_idx"] -= 1
            speed_text.set_text(f"{SPEEDS[state['speed_idx']]}x")
            if state["playing"]:
                start_anim()
        fig.canvas.draw_idle()

    def on_faster(event):
        if state["speed_idx"] < len(SPEEDS) - 1:
            state["speed_idx"] += 1
            speed_text.set_text(f"{SPEEDS[state['speed_idx']]}x")
            if state["playing"]:
                start_anim()
        fig.canvas.draw_idle()

    slider.on_changed(on_slider)
    btn_play.on_clicked(on_play)
    btn_slower.on_clicked(on_slower)
    btn_faster.on_clicked(on_faster)

    plt.show()


def snapshot(df, frame_id, path="snapshot.png",
             show_skeleton=True, show_delaunay=True, show_hull=True):
    """Salva um frame específico como PNG."""
    from mplsoccer import Pitch

    pitch = Pitch(**PITCH_KWARGS)
    fig, ax = pitch.draw(figsize=(14, 9))
    fig.patch.set_facecolor("#111111")

    frame_df = get_frame(df, frame_id)
    draw_frame(ax, frame_df, show_skeleton, show_delaunay, show_hull)

    ts = frame_df.iloc[0]["timestamp"]
    ax.set_title(f"Frame {frame_id}  |  {ts:.1f}s",
                 color="white", fontsize=11, pad=8)

    fig.savefig(path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Salvo em {path}")