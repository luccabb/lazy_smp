from multiprocessing import Manager, Pool, cpu_count

import chess

from alpha_beta import AlphaBeta


class Layer1ParallelAlphaBeta(AlphaBeta):
    
    def search_move(self, board: chess.Board, depth: int, null_move: bool) -> str:
        # creating pool of processes
        nprocs = cpu_count()
        pool = Pool(processes=nprocs)

        manager = Manager()
        # create shared hash table
        shared_hash_table = manager.dict()
        # creating list of moves at layer 1
        arguments = [(board, move, depth, null_move, shared_hash_table) for move in board.legal_moves]
        # executing all the moves at layer 1 in parallel
        # starmap blocks until all process are done
        result = pool.starmap(self.get_black_pieces_best_move, arguments)

        result = sorted(result, key = lambda a: a[1])

        # sorting output and getting best move
        best_move = result[0][2]

        return best_move
