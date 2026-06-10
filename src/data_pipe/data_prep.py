"""
data_prep.py — ButtonTactics Pro
Pipeline de ingestão e preparação dos dados de tracking.

Entrada : kloppy TrackingDataset (Metrica open data)
Saída   : DataFrame limpo com uma linha por jogador por frame
"""

import numpy as np
import pandas as pd
from kloppy import metrica

from src.data_pipe.filters import smooth_positions
from src.core.metrics import add_speed

PITCH_LENGTH = 105.0
PITCH_WIDTH  = 68.0

# ── Carregamento ──────────────────────────────────────────────────────────────

def load_dataset(match_id: int = 1, limit: int | None = None) -> object:
    """
    Carrega os dados de tracking via kloppy (Metrica open data).
    Coordenadas normalizadas [0,1] → convertidas para metros internamente.
    """
    return metrica.load_open_data(match_id=match_id, limit=limit)


# ── Construção do DataFrame ───────────────────────────────────────────────────

def build_dataframe(dataset) -> pd.DataFrame:
    """
    Transforma o TrackingDataset num DataFrame plano.

    Colunas resultantes
    -------------------
    frame_id   : int   — identificador do frame
    period_id  : int   — 1 = primeiro tempo, 2 = segundo tempo
    timestamp  : float — segundos desde o início do período
    player_id  : str   — ex: "home_11"
    team       : str   — "home" ou "away"
    x          : float — posição horizontal em metros (0 = linha de fundo esquerda)
    y          : float — posição vertical em metros   (0 = linha lateral inferior)
    ball_x     : float — posição da bola (metros)
    ball_y     : float
    ball_alive : bool  — True se a bola está em jogo
    """
    rows = []

    for frame in dataset:
        ball = frame.ball_coordinates
        ball_x = ball.x * PITCH_LENGTH if ball else np.nan
        ball_y = ball.y * PITCH_WIDTH  if ball else np.nan
        ball_alive = frame.ball_state is None  # Metrica não informa diretamente

        for player, coord in frame.players_coordinates.items():
            if coord is None:
                continue
            rows.append({
                "frame_id"   : frame.frame_id,
                "period_id"  : frame.period.id,
                "timestamp"  : frame.timestamp.total_seconds(),
                "player_id"  : player.player_id,
                "team"       : player.team.team_id,
                "x"          : coord.x * PITCH_LENGTH,
                "y"          : coord.y * PITCH_WIDTH,
                "ball_x"     : ball_x,
                "ball_y"     : ball_y,
                "ball_alive" : ball_alive,
            })

    return pd.DataFrame(rows)

# ── Pipeline principal ────────────────────────────────────────────────────────

def prepare(match_id: int = 1, limit: int | None = None,
            smooth_window: int = 5) -> pd.DataFrame:
    """
    Executa o pipeline completo:
        load → build DataFrame → smooth → add speed

    Retorna o DataFrame pronto para a camada de visualização.
    """
    dataset = load_dataset(match_id=match_id, limit=limit)
    df = build_dataframe(dataset)
    df = smooth_positions(df, window=smooth_window)
    df = add_speed(df)
    return df


# ── Helpers para a camada de visualização ────────────────────────────────────

def get_frame(df: pd.DataFrame, frame_id: int) -> pd.DataFrame:
    """Retorna todas as linhas de um frame específico."""
    return df[df["frame_id"] == frame_id]


def get_team(df: pd.DataFrame, frame_id: int, team: str) -> pd.DataFrame:
    """Retorna os jogadores de um time em um frame específico."""
    return df[(df["frame_id"] == frame_id) & (df["team"] == team)]


def frame_ids(df: pd.DataFrame) -> np.ndarray:
    """Lista ordenada de frame_ids únicos no dataset."""
    return np.sort(df["frame_id"].unique())