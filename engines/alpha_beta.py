from multiprocessing import Manager
from typing import Tuple, Union

from chess import Board, Move

from engines.base_engine import ChessEngine
from constants import (
    CHECKMATE_SCORE,
    CHECKMATE_THRESHOLD,
    NULL_MOVE_R,
    QUIESCENCE_SEARCH_DEPTH,
)
from move_ordering import organize_moves, organize_moves_quiescence
from psqt import board_evaluation


class AlphaBeta(ChessEngine):
    """
    A class that implements alpha-beta search algorithm.
    """

    def quiescence_search(
        self, board: Board, alpha: float, beta: float, depth: int
    ) -> float:
        """
        This functions extends our search for important
        positions (such as: captures, pawn moves, promotions),
        by using a reduced search tree.

        Arguments:
            - board: chess board state
            - alpha: best score for the maximizing player (best choice (highest value)  we've found
            along the path for max)
            - beta: best score for the minimizing player (best choice (lowest value) we've found
            along the path for min). When Alpha is higher than or equal to Beta, we can prune the search tree;
            because it means that the maximizing player won't find a better move in this branch.
            - depth: how many depths we want to calculate for this board

        Returns:
            - best_score: returns best move's score.
        """
        if board.is_stalemate():
            return 0

        if board.is_checkmate():
            return -CHECKMATE_SCORE

        stand_pat = board_evaluation(board)

        # recursion base case
        if depth == 0:
            return stand_pat

        # beta-cutoff
        if stand_pat >= beta:
            return beta

        # alpha update
        if alpha < stand_pat:
            alpha = stand_pat

        # get moves for quiescence search
        moves = organize_moves_quiescence(board)

        for move in moves:
            # make move and get score
            board.push(move)
            score = -self.quiescence_search(board, -beta, -alpha, depth - 1)
            board.pop()

            # beta-cutoff
            if score >= beta:
                return beta

            # alpha-update
            if score > alpha:
                alpha = score

        return alpha

    def negamax(
        self,
        board: Board,
        depth: int,
        null_move: bool,
        cache: Manager,
        alpha: float = float("-inf"),
        beta: float = float("inf"),
    ) -> Tuple[Union[int, Move]]:
        """
        This functions receives a board, depth and a player; and it returns
        the best move for the current board based on how many depths we're looking ahead
        and which player is playing. Alpha and beta are used to prune the search tree.
        Alpha represents the best score for the maximizing player (best choice (highest value)  we've found
        along the path for max) and beta represents the best score for the minimizing player
        (best choice (lowest value) we've found along the path for min). When Alpha is higher
        than or equal to Beta, we can prune the search tree; because it means that the
        maximizing player won't find a better move in this branch.

        OBS:
            - We only need to evaluate the value for leaf nodes because they are our final states
            of the board and therefore we need to use their values to base our decision of what is
            the best move.

        Arguments:
            - board: chess board state
            - depth: how many depths we want to calculate for this board
            - null_move: if we want to use null move pruning
            - cache: a shared hash table to store the best
                move for each board state and depth.
            - alpha: best score for the maximizing player (best choice
                (highest value)  we've found along the path for max)
            - beta: best score for the minimizing player (best choice
                (lowest value) we've found along the path for min).

        Returns:
            - best_score, best_move: returns best move that it found and its value.
        """

        # check if board was already evaluated
        if (board.fen(), depth) in cache:
            return cache[(board.fen(), depth)]

        if board.is_checkmate():
            cache[(board.fen(), depth)] = (-CHECKMATE_SCORE, None)
            return (-CHECKMATE_SCORE, None)

        if board.is_stalemate():
            cache[(board.fen(), depth)] = (0, None)
            return (0, None)

        # recursion base case
        if depth <= 0:
            # evaluate current board
            board_score = self.quiescence_search(
                board, alpha, beta, QUIESCENCE_SEARCH_DEPTH
            )
            cache[(board.fen(), depth)] = (board_score, None)
            return board_score, None

        # null move prunning
        if null_move and depth >= (NULL_MOVE_R + 1) and not board.is_check():
            board_score = board_evaluation(board)
            if board_score >= beta:
                board.push(Move.null())
                board_score = -self.negamax(
                    board, depth - 1 - NULL_MOVE_R, False, cache, -beta, -beta + 1
                )[0]
                board.pop()
                if board_score >= beta:
                    cache[(board.fen(), depth)] = (beta, None)
                    return beta, None

        best_move = None

        # initializing best_score
        best_score = float("-inf")
        moves = organize_moves(board)

        for move in moves:
            # make the move
            board.push(move)

            board_score = -self.negamax(
                board, depth - 1, null_move, cache, -beta, -alpha
            )[0]
            if board_score > CHECKMATE_THRESHOLD:
                board_score -= 1
            if board_score < -CHECKMATE_THRESHOLD:
                board_score += 1

            # take move back
            board.pop()

            # beta-cutoff
            if board_score >= beta:
                cache[(board.fen(), depth)] = (board_score, move)
                return board_score, move

            # update best move
            if board_score > best_score:
                best_score = board_score
                best_move = move

            # setting alpha variable to do pruning
            alpha = max(alpha, board_score)

            # alpha beta pruning when we already found a solution that is at least as good as the current one
            # those branches won't be able to influence the final decision so we don't need to waste time analyzing them
            if alpha >= beta:
                break

        # if no best move, make a random one
        if not best_move:
            best_move = self.random_move(board)

        # save result before returning
        cache[(board.fen(), depth)] = (best_score, best_move)
        return best_score, best_move

    def search_move(
        self, board: Board, depth: int, null_move: bool
    ) -> Tuple[Union[int, Move]]:
        # create shared cache
        manager = Manager()
        cache = manager.dict()

        return self.negamax(board, depth, null_move, cache)[1]
