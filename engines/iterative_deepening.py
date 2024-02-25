from engines.alpha_beta import AlphaBeta
from typing import Optional, Tuple, Dict
from chess import Board, Move
from move_ordering import organize_moves
from functools import partial
import time 


CACHE_KEY = Dict[Tuple[str, int, bool, float, float], Tuple[float | int, Optional[str]]]


class IterativeDeepening(AlphaBeta):

    def search_move(self, board: Board) -> Move:
        best_move = None
        good_moves = []
        cache: CACHE_KEY = {}
        good_moves_first = partial(organize_moves, good_moves=[])

        start_time = time.monotonic()
        think = 6

        for depth in range(1, 2000):
            _, best_move = self.negamax(
                board=board,
                depth=depth,
                null_move=self.config.null_move,
                cache=cache,
                organize_moves=good_moves_first,
            )
            if best_move in good_moves:
                good_moves.remove(best_move)
            good_moves.insert(0, best_move)
            good_moves_first = partial(organize_moves, good_moves=good_moves)
            end_time = time.monotonic()
            print(f"info depth {depth} time {end_time - start_time:.2f}")
            if end_time - start_time > think:
                break

        return best_move
