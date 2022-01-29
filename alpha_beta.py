from chess import Board, Move
from typing import Tuple, Union
from move_ordering import organize_moves
from quiescence import quiescence_search
from base_engine import ChessEngine
from psqt import board_evaluation
from multiprocessing import Manager
from constants import CHECKMATE_SCORE, CHECKMATE_THRESHOLD, NULL_MOVE_R, QUIESCENCE_SEARCH_DEPTH


class AlphaBeta(ChessEngine):


    def negamax(
        self, 
        board: Board, 
        depth: int, 
        null_move: bool,
        shared_hash_table: Manager,
        alpha: float = float("-inf"), 
        beta: float = float("inf")) -> Tuple[Union[int, Move]]:
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
            - player: player that is currently moving pieces. 1 for AI (max), -1 for human (min).

        Returns:
            - best_score, best_move: returns best move that it found and its value.
        """

        # check if board was already evaluated
        if (board.fen(), depth) in shared_hash_table:
            return shared_hash_table[(board.fen(), depth)]
            
        if board.is_checkmate():
            shared_hash_table[(board.fen(), depth)] = (-CHECKMATE_SCORE, None)
            return (-CHECKMATE_SCORE, None)
        
        if board.is_stalemate():
            shared_hash_table[(board.fen(), depth)] = (0, None)
            return (0, None)

        # recursion base case
        if depth <= 0:
            # evaluate current board
            board_score = quiescence_search(board, alpha, beta, QUIESCENCE_SEARCH_DEPTH)
            shared_hash_table[(board.fen(), depth)] = (board_score, None)
            return board_score, None

        # null move prunning
        if null_move and depth >= (NULL_MOVE_R+1) and not board.is_check():
            board_score = board_evaluation(board)
            if board_score >= beta:
                board.push(Move.null())
                board_score = -self.negamax(board, depth -1 - NULL_MOVE_R, False, shared_hash_table, -beta, -beta+1)[0]
                board.pop()
                if board_score >= beta:
                    shared_hash_table[(board.fen(), depth)] = (beta, None)
                    return beta, None

        best_move = None

        # initializing best_score
        best_score = float("-inf")
        moves = organize_moves(board)
        
        for move in moves:

            # make the move
            board.push(move)

            board_score = -self.negamax(board, depth-1, null_move, shared_hash_table, -beta, -alpha)[0]
            if board_score > CHECKMATE_THRESHOLD:
                board_score -= 1
            if board_score < -CHECKMATE_THRESHOLD:
                board_score += 1

            # take move back
            board.pop()

            # beta-cutoff
            if board_score >= beta:
                shared_hash_table[(board.fen(), depth)] = (board_score, move)
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

        # if it returned no best move, we make a random one
        if not best_move:
            best_move = self.random_move(board)

        # add to hash table before returning
        shared_hash_table[(board.fen(), depth)] = (best_score, best_move)
        return best_score, best_move


    def get_black_pieces_best_move(self, board: Board, move: Move, depth: int, null_move: bool, shared_hash_table: Manager) -> Tuple[Union[int, Move]]:
        # make move
        board.push(move)

        if board.is_checkmate():
            board.pop()
            return board, -CHECKMATE_SCORE*2, move

        value = self.negamax(board, depth-1, null_move, shared_hash_table)[0]

        # remove move
        board.pop()

        return board, value, move


    def search_move(self, board: Board, depth: int, null_move: bool) -> Tuple[Union[int, Move]]:
        manager = Manager()
        # create shared hash table
        shared_hash_table = manager.dict()

        return self.negamax(board, depth, null_move, shared_hash_table)[1]
