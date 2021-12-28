import chess
from collections import defaultdict
from typing import Dict

def build_fen_history(board: chess.Board):
    """
    Creates a history of the board state.
    """
    fen_history = defaultdict(int)
    for move in board.move_stack:
        fen_history[board] += 1
    return fen_history

def check_threefold_repetition(fen_history: Dict[str, int], fen: str) -> bool:
    """
    Checks if the board state is a threefold repetition.
    """
    return fen_history[fen] >= 3