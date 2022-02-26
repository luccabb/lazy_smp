from collections import defaultdict
from copy import copy
from multiprocessing import Manager, Pool, cpu_count
from typing import List, Tuple

from chess import Board, Move

from alpha_beta import AlphaBeta
from constants import CHECKMATE_THRESHOLD

LAYER_SIGNAL_CORRECTION = lambda data: data if data[3] == 2 else (-data[0], *data[1:])
CHECKMATE_CORRECTION = lambda data: (data[0]+1, *data[1:]) if (data[0] > CHECKMATE_THRESHOLD and data[3] == 1) else data


class Layer2ParallelAlphaBeta(AlphaBeta):
    """
    This class implements a parallel search 
    algorithm starting from the second layer.
    """


    def generate_board_and_moves(
        self, 
        og_board: Board, 
        board_to_move_that_generates_it: Manager,
        layer: int) -> List[Tuple[Board, Move]]: 
        """
        Generate all possible boards with their layer depth for each board.

        Args:
            og_board: Board to generate moves for.
            board_to_move_that_generates_it: Dictionary that maps board to move that generates it.
            layer: Layer depth of the board.

        Returns:
            List of tuples with: 
                - generated board (original board with move applied)
                - original board
                - layer depth
        """
        boards_and_moves = []
        board = copy(og_board)

        # if board has no legal moves, we leave it as is
        # we need to run this board through negamax to get its value
        if not og_board.legal_moves:
            boards_and_moves.append((og_board, og_board, layer))

        # get first layer move that generates current board
        if og_board.fen() in board_to_move_that_generates_it:
            first_move = board_to_move_that_generates_it[og_board.fen()]
        else:
            first_move = None
            
        # generating all possible moves
        for move in board.legal_moves:

            board.push(move)

            # save first layer move that generates current board
            if first_move:
                board_to_move_that_generates_it[board.fen()] = first_move
            else:
                board_to_move_that_generates_it[board.fen()] = move
            # add new board, original board, and current layer to our output
            boards_and_moves.append((copy(board), og_board, layer+1))

            board.pop()

        return boards_and_moves
    

    def search_move(
        self, 
        board: Board, 
        depth: int, 
        null_move: bool) -> str:
        START_LAYER = 2

        # creating pool of processes
        nprocs = cpu_count()
        pool = Pool(processes=nprocs)
        manager = Manager()

        # pointer that help us in finding the best next move
        board_to_move_that_generates_it = manager.dict()

        # starting board list
        board_list = [(board, board, 0)]
        
        # generating all possible boards for up to 2 moves ahead
        for _ in range(START_LAYER):
            arguments = [(board, board_to_move_that_generates_it, layer) for board, _, layer in board_list]
            board_list = pool.starmap(self.generate_board_and_moves, arguments)
            board_list = [board for board in sum(board_list, [])]
        
        # negamax arguments
        shared_hash_table = manager.dict()
        arguments = [(board, depth-START_LAYER, null_move, shared_hash_table)
            for board, _, _ in board_list]

        parallel_layer_result = pool.starmap(self.negamax, arguments)

        # grouping output based on the  board that generates it
        groups = defaultdict(list)
        
        # adding information about the board and layer 
        # that generates the results and separating them
        # into groups based on the root board
        for i in range(len(parallel_layer_result)):
            groups[board_list[i][1].fen()].append((*parallel_layer_result[i], board_list[i][0], board_list[i][2]))
        
        best_boards = []

        for group in groups.values():
            # layer and checkmate correections
            # they are needed to adjust for 
            # boards from different layers
            group = list(map(LAYER_SIGNAL_CORRECTION, group))
            group = list(map(CHECKMATE_CORRECTION, group))
            # get best move from group
            group.sort(key = lambda a: a[0])
            best_boards.append(group[0])
        
        # get best board
        best_boards.sort(key = lambda a: a[0], reverse = True)
        best_board = best_boards[0][2].fen()

        # get move that results in best board
        best_move = board_to_move_that_generates_it[best_board]

        return best_move
