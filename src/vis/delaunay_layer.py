from scipy.spatial import Delaunay

def data(pts):
    x_coords, y_coords = [], []
    if len(pts) < 3:
        return x_coords, y_coords
    try:
        tri = Delaunay(pts)
        for simplex in tri.simplices:
            t = pts[simplex]
            for a, b in [(0,1),(1,2),(2,0)]:
                x_coords += [t[a][0], t[b][0], None]
                y_coords += [t[a][1], t[b][1], None]
    except Exception:
        pass
    return x_coords, y_coords
