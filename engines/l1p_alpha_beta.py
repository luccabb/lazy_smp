from copy import copy
from multiprocessing import Manager, Pool, cpu_count

import chess

from engines.alpha_beta import AlphaBeta, negamax_wrapper


class Layer1ParallelAlphaBeta(AlphaBeta):
    """
    This class implements a parallel search
    algorithm starting from the first layer.
    """

    def search_move(self, board: chess.Board) -> str:
        # start multiprocessing
        nprocs = cpu_count()
        pool = Pool(processes=nprocs)
        # manager = Manager()
        # shared_cache = manager.dict()

        # creating list of moves at layer 1
        moves = list(board.legal_moves)
        arguments = []
        for move in moves:
            board.push(move)
            arguments.append(
                (copy(board),
                 copy(self.config.negamax_depth) - 1,
                 self.config.null_move,
                 self,
                #  shared_cache))
                ))
            board.pop()

        # executing all the moves at layer 1 in parallel
        # starmap blocks until all process are done
        processes = pool.starmap(negamax_wrapper, arguments)
        results = []

        # inserting move information in the results
        for i in range(len(processes)):
            results.append((*processes[i], moves[i]))

        # sorting results and getting best move
        results.sort(key=lambda a: a[0])
        best_move = results[0][2]
        return best_move
