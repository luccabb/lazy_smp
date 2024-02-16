from abc import abstractmethod
from typing import Optional

from config import Config

from chess import Board

from typing import Protocol


class ChessEngine(Protocol):
    """
    A class to represent a chess engine.

    Methods:
        - random_move: returns a random move from the list of legal moves.
        - search_move: returns the best move for
        the current board based on how many depths
        we're looking ahead.
    """
    def __init__(self, config: Config):
        ...

    @abstractmethod
    def search_move(self, board: Board, depth: int, null_move: bool) -> Optional[str]:
        """
        We'll search for the best possible move in the board that we're
        receiving up to a given depth.

        Arguments:
            - board: chess board state.
            - depth: maximum depth to search.
            - null_move: if we're using null move pruning in our search.

        Returns:
            - move: the best move found.
        """
        raise NotImplementedError()
