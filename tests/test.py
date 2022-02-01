import unittest
from chess import Board, Move
from parameterized import parameterized
from helper import get_engine


test_count_pieces = [
    (Board("rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1"), (16, 16)),
    (Board("rnbqkbnr/pppppppp/8/8/8/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1"), (16, 15)),
    (Board("2b1k1n1/p3p1pp/1PP5/1Nr2P2/1p1p1p2/2b4B/P1PQP2P/R1B1K1NR w KQ - 0 1"), (12, 15)),
    (Board("4k3/7p/8/8/8/8/8/R3K1NR w KQ - 0 1"), (2, 4)),
    (Board("4k3/8/8/8/8/8/8/4K3 w - - 0 1"), (1, 1)),
    (Board("8/8/8/8/8/8/8/8 w - - 0 1"), (0, 0)),
]


test_board_value = [
    (Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"), 0),
    (Board("rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1"), -0.07),
    (Board("rnbqkbnr/pppppppp/8/8/8/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1"), +2.00),
    (Board("2b1k1n1/p3p1pp/1PP5/1Nr2P2/1p1p1p2/2b4B/P1PQP2P/R1B1K1NR w KQ - 0 1"), -43.87),
    (Board("4k3/7p/8/8/8/8/8/R3K1NR w KQ - 0 1"), -34.00),
    (Board("4k3/8/8/8/8/8/8/4K3 w - - 0 1"), 0.00),
    (Board("8/8/8/8/8/8/8/8 w - - 0 1"), 0.00),
]


test_get_move_score = [
    (Board("4R2k/8/8/8/8/7R/8/3K4 b - - 0 1"), 1, True, [Move.from_uci('h8g7')]),
    (Board("4R2k/8/8/8/8/7R/8/3K4 w - - 0 1"), 1, False, [Move.from_uci('e8h8')]),
    (Board("7k/8/8/8/3n4/7q/8/7K b - - 0 1"), 2, True, [Move.from_uci('d4f3')]),
    (Board("7k/8/8/8/8/1r6/r7/2K5 b - - 0 1"), 3, True, [Move.from_uci('a2f2'), Move.from_uci('h8g8'), Move.from_uci('h8g7'), Move.from_uci('b3b2')]),
    (Board("rnbqkbnr/pppp1ppp/8/4p3/5PP1/8/PPPPP2P/RNBQKBNR b KQkq - 0 1"), 2, True, [Move.from_uci('d8h4')]),
    (Board("rnb1k1nr/ppp2ppp/3b4/8/8/2N3q1/PPPPP2P/R1BQKBNR w KQkq - 0 1"), 3, False, [Move.from_uci('h2g3')]),
]


test_boards = [
    (Board("4r2K/8/8/8/8/7r/8/3k4 w - - 0 1"), 1, [Move.from_uci('h8g7')]),
    (Board("8/8/8/6K1/8/5r2/8/2k3r1 w - - 0 1"), 4, [Move.from_uci('g5h4')]),
    (Board("7K/8/8/8/6Q1/8/4N3/7k w - - 0 1"), 1, [Move.from_uci('g4h3'), Move.from_uci('g4g1')]),
    (Board("7K/8/8/8/3N4/7Q/7p/7k w - - 0 1"), 2, [Move.from_uci('h3f1')]),
    (Board("7K/8/8/8/8/1R6/5R2/3k4 w - - 0 1"), 2, [Move.from_uci('b3b1')]),
    (Board("7K/8/8/8/8/1R6/R7/2k5 w - - 0 1"), 3, [Move.from_uci('h8h7'), Move.from_uci('a2h2'), Move.from_uci('b3b4'), Move.from_uci('b3b5'), Move.from_uci('b3b6'), Move.from_uci('b3b7'), Move.from_uci('b3b4'), Move.from_uci('a2g2'), Move.from_uci('a2f2'), Move.from_uci('b3b8'), Move.from_uci('h8g8'), Move.from_uci('h8g7'), Move.from_uci('b3b2')]),
    (Board("rnbqkbnr/ppppp2p/8/5pp1/4P3/8/PPPP1PPP/RNBQKBNR w KQk - 0 1"), 2, [Move.from_uci('d1h5')]),

    (Board("4R2k/8/8/8/8/7R/8/3K4 b - - 0 1"), 1, [Move.from_uci('h8g7')]),
    (Board("8/8/8/6k1/8/5R2/8/2K3R1 b - - 0 1"), 4, [Move.from_uci('g5h4')]),
    (Board("7k/8/8/8/6q1/8/4n3/7K b - - 0 1"), 1, [Move.from_uci('g4h3'), Move.from_uci('g4g1')]),
    (Board("7k/8/8/8/3n4/7q/7P/7K b - - 0 1"), 2, [Move.from_uci('h3f1')]),
    (Board("7k/8/8/8/8/1r6/5r2/3K4 b - - 0 1"), 2, [Move.from_uci('b3b1')]),
    (Board("7k/8/8/8/8/1r6/r7/2K5 b - - 0 1"), 3, [Move.from_uci('h8h7'), Move.from_uci('a2h2'), Move.from_uci('b3b4'), Move.from_uci('b3b5'), Move.from_uci('b3b6'), Move.from_uci('b3b7'), Move.from_uci('b3b4'), Move.from_uci('a2g2'), Move.from_uci('a2f2'), Move.from_uci('b3b8'), Move.from_uci('h8g8'), Move.from_uci('h8g7'), Move.from_uci('b3b2')]),
    (Board("rnbqkbnr/pppp1ppp/8/4p3/5PP1/8/PPPPP2P/RNBQKBNR b KQkq - 0 1"), 2, [Move.from_uci('d8h4')]),
]

class Testunctions(unittest.TestCase):


    @parameterized.expand(test_boards)
    def test_alpha_beta(self, board, depth, expected_result):
        ALGORITHM_NAME = "alpha_beta"
        NULL_MOVE = False

        engine = get_engine(ALGORITHM_NAME)
        result = engine.search_move(board, depth, NULL_MOVE)
        self.assertIn(result, expected_result)
    

    @parameterized.expand(test_boards)
    def test_parallel_alpha_beta_layer_1(self, board, depth, expected_result):
        ALGORITHM_NAME = "parallel_alpha_beta_layer_1"
        NULL_MOVE = False

        engine = get_engine(ALGORITHM_NAME)
        result = engine.search_move(board, depth, NULL_MOVE)
        self.assertIn(result, expected_result)


    @parameterized.expand(test_boards)
    def test_parallel_alpha_beta_layer_2(self, board, depth, expected_result):
        ALGORITHM_NAME = "parallel_alpha_beta_layer_2"
        NULL_MOVE = False

        engine = get_engine(ALGORITHM_NAME)
        result = engine.search_move(board, depth, NULL_MOVE)
        self.assertIn(result, expected_result)


    @parameterized.expand(test_boards)
    def test_lazy_smp(self, board, depth, expected_result):
        ALGORITHM_NAME = "lazy_smp"
        NULL_MOVE = False

        engine = get_engine(ALGORITHM_NAME)
        result = engine.search_move(board, depth, NULL_MOVE)
        self.assertIn(result, expected_result)


if __name__ == '__main__':
    unittest.main()