import numpy as np

from src.config.settings import PITCH_LENGTH, PITCH_WIDTH


def _split_three_lines(depths: np.ndarray) -> tuple[int, int, int]:
    """Split sorted outfield depths into 3 contiguous tactical lines."""
    n = len(depths)
    if n < 6:
        base = n // 3
        rem = n % 3
        return base + (1 if rem > 0 else 0), base + (1 if rem > 1 else 0), base

    csum = np.concatenate(([0.0], np.cumsum(depths)))
    csum2 = np.concatenate(([0.0], np.cumsum(depths * depths)))

    def sse(a: int, b: int) -> float:
        seg_n = b - a
        seg_sum = csum[b] - csum[a]
        seg_sum2 = csum2[b] - csum2[a]
        mean = seg_sum / seg_n
        return float(seg_sum2 - 2.0 * mean * seg_sum + seg_n * mean * mean)

    best = (4, 3, n - 7)
    best_score = np.inf

    for i in range(2, n - 3):
        for j in range(i + 2, n - 1):
            c1, c2, c3 = i, j - i, n - j
            if c1 < 2 or c2 < 2 or c3 < 2:
                continue

            score = sse(0, i) + sse(i, j) + sse(j, n)

            # Penalize unlikely tactical line sizes to stabilize noisy frames.
            if c1 > 5 or c2 > 5 or c3 > 5:
                score += 1e6
            score += 50.0 * abs(c1 - 4)
            score += 35.0 * abs(c2 - 3)
            score += 35.0 * abs(c3 - 3)

            if score < best_score:
                best_score = score
                best = (c1, c2, c3)

    return best


def _lines_data(pts):
    """
    Infer and draw tactical formation lines from team positions.

    Returns
    -------
    x_coords, y_coords : list, list
        Polyline coordinates (with None separators) for each tactical line.
    label_x, label_y : float | None, float | None
        Anchor point for formation text.
    formation : str
        Formation string such as "4-3-3".
    """
    x_coords, y_coords = [], []
    if len(pts) < 6:
        return x_coords, y_coords, None, None, ""

    p = np.asarray(pts, dtype=float)
    x = p[:, 0]

    # Infer defending side from which pitch edge has the deepest player.
    left_gap = float(np.min(x))
    right_gap = float(PITCH_LENGTH - np.max(x))
    defends_left = left_gap <= right_gap

    depth = x if defends_left else (PITCH_LENGTH - x)

    # Remove goalkeeper: deepest player relative to own goal.
    gk_idx = int(np.argmin(depth))
    mask = np.ones(len(p), dtype=bool)
    mask[gk_idx] = False
    outfield = p[mask]
    out_depth = depth[mask]

    order = np.argsort(out_depth)
    sorted_pts = outfield[order]
    sorted_depth = out_depth[order]

    c1, c2, c3 = _split_three_lines(sorted_depth)
    cuts = (c1, c1 + c2)
    groups = [sorted_pts[:cuts[0]], sorted_pts[cuts[0]:cuts[1]], sorted_pts[cuts[1]:]]

    for grp in groups:
        if len(grp) < 2:
            continue
        line = grp[np.argsort(grp[:, 1])]
        for i in range(len(line) - 1):
            x_coords += [float(line[i, 0]), float(line[i + 1, 0]), None]
            y_coords += [float(line[i, 1]), float(line[i + 1, 1]), None]

    formation = f"{len(groups[0])}-{len(groups[1])}-{len(groups[2])}"

    team_center_x = float(np.mean(outfield[:, 0]))
    y_min = float(np.min(outfield[:, 1]))
    y_max = float(np.max(outfield[:, 1]))
    if (y_min + y_max) / 2.0 > (PITCH_WIDTH / 2.0):
        label_y = max(1.0, y_min - 2.0)
    else:
        label_y = min(PITCH_WIDTH - 1.0, y_max + 2.0)

    return x_coords, y_coords, team_center_x, label_y, formation