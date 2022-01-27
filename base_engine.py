from abc import abstractmethod
from chess import Board


class ChessEngine():

    @abstractmethod
    def search_move(self, board: Board, depth: int, null_move: bool) -> str:
        return
