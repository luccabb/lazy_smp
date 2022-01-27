from abc import abstractmethod
from chess import Board
from random import choice


class ChessEngine():

    def random_move(self, board: Board):
        """
        Returns a random move from the list of legal moves.

        Arguments:
            - board: chess board state.

        Returns:
            - move: a random move from the list of legal moves.
        """
        move = choice([move for move in board.legal_moves])
        return move


    @abstractmethod
    def search_move(self, board: Board, depth: int, null_move: bool) -> str:
        return
