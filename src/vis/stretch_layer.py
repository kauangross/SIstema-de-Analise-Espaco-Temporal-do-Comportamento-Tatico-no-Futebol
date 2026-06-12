import numpy as np
import streamlit as st
from src.config.settings import PITCH_LENGTH, PITCH_WIDTH
from vis.lines_layer import _split_three_lines


@st.cache_data
def _stretch_index(pts):
	"""Calcula o Stretch Index da linha defensiva no intervalo [0, 1]."""
	if len(pts) < 6:
		return None

	p = np.asarray(pts, dtype=float)
	x = p[:, 0]

	left_gap = float(np.min(x))
	right_gap = float(PITCH_LENGTH - np.max(x))
	defends_left = left_gap <= right_gap
	depth = x if defends_left else (PITCH_LENGTH - x)

	# Remove o provável goleiro (jogador mais profundo em relação ao próprio gol).
	gk_idx = int(np.argmin(depth))
	outfield_mask = np.ones(len(p), dtype=bool)
	outfield_mask[gk_idx] = False
	outfield = p[outfield_mask]
	out_depth = depth[outfield_mask]

	if len(outfield) < 6:
		return None

	order = np.argsort(out_depth)
	sorted_pts = outfield[order]
	sorted_depth = out_depth[order]

	n_def, _, _ = _split_three_lines(sorted_depth)
	defenders = sorted_pts[:n_def]
	if len(defenders) < 2:
		return 0.0

	lateral_span = float(np.max(defenders[:, 1]) - np.min(defenders[:, 1]))
	stretch = lateral_span / PITCH_WIDTH
	return float(np.clip(stretch, 0.0, 1.0))

@st.cache_data
def _defensive_line_data(pts):
    x_coords, y_coords = [], []
    if len(pts) < 6:
        return x_coords, y_coords

    p = np.asarray(pts, dtype=float)
    x = p[:, 0]

    left_gap = float(np.min(x))
    right_gap = float(PITCH_LENGTH - np.max(x))
    defends_left = left_gap <= right_gap
    depth = x if defends_left else (PITCH_LENGTH - x)

    gk_idx = int(np.argmin(depth))
    mask = np.ones(len(p), dtype=bool)
    mask[gk_idx] = False
    outfield = p[mask]
    out_depth = depth[mask]

    order = np.argsort(out_depth)
    sorted_pts = outfield[order]
    sorted_depth = out_depth[order]

    c1, _, _ = _split_three_lines(sorted_depth)
    defenders = sorted_pts[:c1]

    if len(defenders) < 2:
        return x_coords, y_coords

    line = defenders[np.argsort(defenders[:, 1])]
    for i in range(len(line) - 1):
        x_coords += [float(line[i, 0]), float(line[i + 1, 0]), None]
        y_coords += [float(line[i, 1]), float(line[i + 1, 1]), None]

    return x_coords, y_coords