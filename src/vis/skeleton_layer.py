import numpy as np
    
import streamlit as st
@st.cache_data
def _skeleton_data(pts):
    x_coords, y_coords = [], []
    if len(pts) < 2:
        return x_coords, y_coords
    for i, p in enumerate(pts):
        dists = np.linalg.norm(pts - p, axis=1)
        dists[i] = np.inf
        for j in np.argsort(dists)[:2]:
            x_coords += [p[0], pts[j][0], None]
            y_coords += [p[1], pts[j][1], None]
    return x_coords, y_coords