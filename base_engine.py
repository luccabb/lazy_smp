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
        """
        We'll search for the best possible move in the board that we're
        receiving up to a given depth. This

        Arguments:
            - board: chess board state.
            - depth: maximum depth to search.
            - null_move: if we're using null move pruning in our search.

        Returns:
            - move: the best move found.
        """
        raise NotImplementedError()
