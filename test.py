import unittest
import chess
from parameterized import parameterized

import main

test_count_pieces = [
    (chess.Board("rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1"), (16, 16)),
    (chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1"), (16, 15)),
    (chess.Board("2b1k1n1/p3p1pp/1PP5/1Nr2P2/1p1p1p2/2b4B/P1PQP2P/R1B1K1NR w KQ - 0 1"), (12, 15)),
    (chess.Board("4k3/7p/8/8/8/8/8/R3K1NR w KQ - 0 1"), (2, 4)),
    (chess.Board("4k3/8/8/8/8/8/8/4K3 w - - 0 1"), (1, 1)),
    (chess.Board("8/8/8/8/8/8/8/8 w - - 0 1"), (0, 0)),
]

test_board_value = [
    (chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"), 0),
    (chess.Board("rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1"), -0.07),
    (chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1"), +2.00),
    (chess.Board("2b1k1n1/p3p1pp/1PP5/1Nr2P2/1p1p1p2/2b4B/P1PQP2P/R1B1K1NR w KQ - 0 1"), -43.87),
    (chess.Board("4k3/7p/8/8/8/8/8/R3K1NR w KQ - 0 1"), -34.00),
    (chess.Board("4k3/8/8/8/8/8/8/4K3 w - - 0 1"), 0.00),
    (chess.Board("8/8/8/8/8/8/8/8 w - - 0 1"), 0.00),
]

test_get_move_score = [
    (chess.Board("4R2k/8/8/8/8/7R/8/3K4 b - - 0 1"), 1, True, [chess.Move.from_uci('h8g7')]),
    (chess.Board("4R2k/8/8/8/8/7R/8/3K4 w - - 0 1"), 1, False, [chess.Move.from_uci('e8h8')]),
    (chess.Board("7k/8/8/8/3n4/7q/8/7K b - - 0 1"), 2, True, [chess.Move.from_uci('d4f3')]),
    (chess.Board("7k/8/8/8/8/1r6/r7/2K5 b - - 0 1"), 3, True, [chess.Move.from_uci('a2f2'), chess.Move.from_uci('h8g8'), chess.Move.from_uci('h8g7'), chess.Move.from_uci('b3b2')]),
    (chess.Board("rnbqkbnr/pppp1ppp/8/4p3/5PP1/8/PPPPP2P/RNBQKBNR b KQkq - 0 1"), 2, True, [chess.Move.from_uci('d8h4')]),
    (chess.Board("rnb1k1nr/ppp2ppp/3b4/8/8/2N3q1/PPPPP2P/R1BQKBNR w KQkq - 0 1"), 3, False, [chess.Move.from_uci('h2g3')]),
]

class TestChessFunctions(unittest.TestCase):

    @parameterized.expand(test_count_pieces)
    def test_count_pieces(self, fen, expected_result):
        result = main.count_pieces(fen)
        self.assertEqual(result, expected_result)


    @parameterized.expand(test_board_value)
    def test_board_value(self, fen, expected_result):
        result = main.board_value(fen)
        self.assertEqual(result, expected_result)
    

    @parameterized.expand(test_get_move_score)
    def test_get_move_score(self, fen, depth, player, expected_result):
        result = main.get_move_score(fen, depth, player)
        self.assertIn(result[1], expected_result)

if __name__ == '__main__':
    unittest.main()