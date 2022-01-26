import chess
from typing import Tuple, Union
from multiprocessing import cpu_count, connection, Manager, Process
from random import choice
import move_ordering
from quiescence import quiescence_search
from base_engine import ChessEngine
from psqt import board_evaluation
from helper import CHECKMATE_SCORE, CHECKMATE_THRESHOLD, NULL_MOVE_R


class AlphaBeta(ChessEngine):
    def negamax(
        self, 
        board: chess.Board, 
        depth: int, 
        null_move: bool,
        alpha: float = float("-inf"), 
        beta: float = float("inf")) -> Tuple[Union[int, chess.Move]]:
        """
        This functions receives a board, depth and a player; and it returns
        the best move for the current board based on how many depths we're looking ahead
        and which player is playing. Alpha and beta are used to prune the search tree.
        Alpha represents the best score for the maximizing player (best choice (highest value)  we've found 
        along the path for max) and beta represents the best score for the minimizing player
        (best choice (lowest value) we've found along the path for min). When Alpha is higher 
        than or equal to Beta, we can prune the search  tree; because it means that the 
        maximizing player won't find a better move in this branch.

        OBS:
            - We only need to evaluate the value for leaf nodes because they are our final states
            of the board and therefore we need to use their values to base our decision of what is 
            the best move.

        Arguments: 
            - board: chess board state
            - depth: how many depths we want to calculate for this board
            - player: player that is currently moving pieces. 1 for AI (max), -1 for human (min).

        Returns:
            - best_score, best_move: returns best move that it found and its value.
        """

        if board.is_checkmate():
            return (-CHECKMATE_SCORE, None)

        if board.is_stalemate():
            return (0, None)

        # recursion base case
        if depth <= 0:
            # evaluate current board
            board_value = quiescence_search(board, alpha, beta, 2) 
            return board_value, None

        # null move prunning
        if null_move and depth >= (NULL_MOVE_R+1) and not board.is_checkmate():
            board_value = board_evaluation(board)
            if board_value >= beta:
                board.push(chess.Move.null())
                board_value = -self.negamax(board, depth -1 - NULL_MOVE_R, False, -beta, -beta+1)[0]
                board.pop()
                if board_value >= beta:
                    return beta, None

        best_move = None

        # initializing best_score
        best_score = float("-inf")
        moves = move_ordering.organize_moves_2(board)
        
        # for move in board.legal_moves:
        for move in moves:
            # make the move
            board.push(move)

            score = -self.negamax(board, depth-1, null_move, -beta, -alpha)[0]
            if score > CHECKMATE_THRESHOLD:
                score -= 1
            if score < -CHECKMATE_THRESHOLD:
                score += 1

            # take move back
            board.pop()

            # beta-cutoff
            if score >= beta:
                return score, move

            # update best move
            if score > best_score:
                best_score = score
                best_move = move
            
            # setting alpha variable to do pruning
            alpha = max(alpha, score)

            # alpha beta pruning when we already found a solution that is at least as good as the current one
            # those branches won't be able to influence the final decision so we don't need to waste time analyzing them
            if alpha >= beta:
                break

        # if it returned no best move, we make a random one
        if not best_move:
            if board.legal_moves:
                best_move = choice([move for move in board.legal_moves])
            else:
                best_move = None
        
        return best_score, best_move

    def search_move(self, board: chess.Board, depth: int, null_move: bool) -> Tuple[Union[int, chess.Move]]:
        return self.negamax(board, depth, null_move)[1].uci()