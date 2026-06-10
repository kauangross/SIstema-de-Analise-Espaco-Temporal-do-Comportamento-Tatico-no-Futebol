import numpy as np
from scipy.spatial import ConvexHull

def _hull_data(pts):
    x_line, y_line, x_fill, y_fill = [], [], [], []
    if len(pts) < 3:
        return x_line, y_line, x_fill, y_fill
    try:
        hull = ConvexHull(pts)
        hp = np.append(hull.vertices, hull.vertices[0])
        x_line = pts[hp, 0].tolist()
        y_line = pts[hp, 1].tolist()
        x_fill = pts[hull.vertices, 0].tolist()
        y_fill = pts[hull.vertices, 1].tolist()
    except Exception:
        pass
    return x_line, y_line, x_fill, y_fill
