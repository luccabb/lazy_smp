from chess import Board, Move
from typing import Tuple, Union
from multiprocessing import cpu_count, Manager, Process
from move_ordering import organize_moves
from quiescence import quiescence_search
from base_engine import ChessEngine
from psqt import board_evaluation
from constants import CHECKMATE_SCORE, CHECKMATE_THRESHOLD, NULL_MOVE_R, QUIESCENCE_SEARCH_DEPTH


class LazySMP(ChessEngine):


    def search_move(self, board: Board, depth: int, null_move: bool) -> str:

        # getting number of processors
        nprocs = cpu_count()

        # start manager so that we can share data between processes
        with Manager() as manager:
            
            # create shared hash table
            shared_hash_table = manager.dict()
            processes = []
            
            # start search for all processors from the root node
            for _ in range(nprocs):
                p = Process(target=self.negamax, args=(board, depth, null_move, shared_hash_table))
                p.start()
                processes.append(p)
            
            # wait for all processes to finish
            for process in processes:
                process.join()

            # close all ongoing processes
            for p in processes:
                p.terminate()
            
            # return best move for our original board
            return shared_hash_table[(board.fen(), depth)][1]