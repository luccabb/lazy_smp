import chess
from typing import Tuple, Union
from multiprocessing import cpu_count, Pool
from alpha_beta import AlphaBeta
from constants import CHECKMATE_SCORE


class Layer1ParallelAlphaBeta(AlphaBeta):
    def get_black_pieces_best_move(self, board: chess.Board, move: chess.Move, depth: int, null_move: bool) -> Tuple[Union[int, chess.Move]]:
        # make move
        board.push(move)

        if board.is_checkmate():
            board.pop()
            return board, -CHECKMATE_SCORE*2, move

        value = self.negamax(board, depth-1, null_move)[0]

        # remove move
        board.pop()

        return board, value, move
    
    def search_move(self, board: chess.Board, depth: int, null_move: bool) -> str:
        # creating pool of processes
        nprocs = cpu_count()
        pool = Pool(processes=nprocs)

        # creating list of moves at layer 1
        arguments = [(board, move, depth, null_move) for move in board.legal_moves]
        # executing all the moves at layer 1 in parallel
        # starmap blocks until all process are done
        result = pool.starmap(self.get_black_pieces_best_move, arguments)

        result = sorted(result, key = lambda a: a[1])

        # sorting output and getting best move
        best_move = result[0][2]

        return best_move