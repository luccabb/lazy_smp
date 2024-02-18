from multiprocessing import Manager, Pool, cpu_count

from chess import Board

from engines.alpha_beta import AlphaBeta, negamax_wrapper, CACHE
from copy import copy


class LazySMP(AlphaBeta):

    def search_move(self, board: Board) -> str:
        # start multiprocessing
        nprocs = cpu_count()
        pool = Pool(processes=nprocs)
        # executing all the moves at layer 1 in parallel
        # starmap blocks until all process are done
        pool.starmap(
            negamax_wrapper,
            [(
                board,
                copy(self.config.negamax_depth),
                self.config.null_move,
                self,
            ) for _ in range(nprocs)],
        )

        # return best move for our original board
        return CACHE[(board.fen(), self.config.negamax_depth, self.config.null_move, float("-inf"), float("inf"))][1]
