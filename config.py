from dataclasses import dataclass

CHECKMATE_SCORE = 10**8
CHECKMATE_THRESHOLD = 999 * (10**4)


@dataclass
class Config:
    """
    Configuration for the engine.
    """
    mode: str
    algorithm: str
    negamax_depth: int
    null_move: bool
    null_move_r: int
    quiescence_search_depth: int
    checkmate_score: int = CHECKMATE_SCORE
    checkmate_threshold: int = CHECKMATE_THRESHOLD
