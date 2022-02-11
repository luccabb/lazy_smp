from multiprocessing import Manager, Pool, cpu_count

from chess import Board

from alpha_beta import AlphaBeta


class LazySMP(AlphaBeta):


    def search_move(self, board: Board, depth: int, null_move: bool) -> str:
        # getting number of processors
        nprocs = cpu_count()
        pool = Pool(processes=nprocs)

        manager = Manager()
        # create shared hash table
        shared_hash_table = manager.dict()
        # executing all the moves at layer 1 in parallel
        # starmap blocks until all process are done
        pool.starmap(self.negamax, [(board, depth, null_move, shared_hash_table) for _ in range(nprocs)])

        # return best move for our original board
        return shared_hash_table[(board.fen(), depth)][1]
