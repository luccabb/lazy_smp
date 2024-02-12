from random import choice

from chess import Board

from typing import Protocol


class RandomEngine(Protocol):

    def search_move(self, board: Board):
        """
        Returns a random move from the list of legal moves.

        Arguments:
            - board: chess board state.

        Returns:
            - move: a random move from the list of legal moves.
        """
        move = choice([move for move in board.legal_moves])
        return move
