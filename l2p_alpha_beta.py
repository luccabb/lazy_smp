import chess
from typing import Tuple, List
from multiprocessing import cpu_count, Pool
from l1p_alpha_beta import Layer1ParallelAlphaBeta


class Layer2ParallelAlphaBeta(Layer1ParallelAlphaBeta):

    def generate_board_and_moves(self, board: List[Tuple[chess.Board, chess.Move]]) -> List[Tuple[chess.Board, chess.Move]]: 
        boards_and_moves = []
        b, og_move = board

        if not b.legal_moves:
            boards_and_moves.append((b, og_move))

        for move in b.legal_moves:
            boards_and_moves.append((b, move))
        return boards_and_moves


    def search_move(self, board: chess.Board, depth: int, null_move: bool) -> str:
        START_LAYER = 2

        # creating pool of processes
        nprocs = cpu_count()
        pool = Pool(processes=nprocs)

        board_list = [(board, None)]
        for _ in range(START_LAYER):
            arguments = [[(board, move)] for board, move in board_list]
            board_list = pool.starmap(self.generate_board_and_moves, arguments)
            board_list = [board_move for board_move in sum(board_list, [])]
        arguments = [(board, move, depth-START_LAYER, null_move)
            for board, move in board_list]

        parallel_layer_result = pool.starmap(self.get_black_pieces_best_move, arguments) # f7f6

        parallel_layer_result.sort(key = lambda a: a[1])
        # sorting output and getting best move
        best_move = parallel_layer_result[0][2]

        return best_move
