import numpy as np
import pandas as pd

# ── Cálculo de velocidade ─────────────────────────────────────────────────────

def add_speed(df: pd.DataFrame, fps: float = 25.0) -> pd.DataFrame:
    """
    Estima a velocidade instantânea (m/s) de cada jogador entre frames consecutivos.
    Valores extremos (> 12 m/s) são descartados como outliers de tracking.
    """
    df = df.sort_values(["player_id", "frame_id"]).copy()

    dx = df.groupby("player_id")["x"].diff()
    dy = df.groupby("player_id")["y"].diff()
    speed = np.sqrt(dx**2 + dy**2) * fps

    speed[speed > 12.0] = np.nan   # limite físico realista
    df["speed"] = speed
    return df