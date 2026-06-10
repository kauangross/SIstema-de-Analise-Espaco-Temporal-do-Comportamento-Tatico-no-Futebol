import pandas as pd

# ── Filtro de suavização ──────────────────────────────────────────────────────

def smooth_positions(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """
    Aplica média móvel (rolling mean) em x e y por jogador para
    reduzir ruído posicional e evitar falsos picos de velocidade.

    window : tamanho da janela em frames (default = 5)
    """
    df = df.sort_values(["player_id", "frame_id"]).copy()

    for col in ("x", "y"):
        df[col] = (
            df.groupby("player_id")[col]
              .transform(lambda s: s.rolling(window, min_periods=1, center=True).mean())
        )

    return df