# flake8: noqa
from typing import List, Tuple

from config import Config
import chess
import chess.syzygy

############
# I'm using Pesto Evaluation function:
# https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function
# values for Piece-Square Tables from Rofchade:
# http://www.talkchess.com/forum3/viewtopic.php?f=2&t=68311&start=19
############
MG_PIECE_VALUES = {
    chess.PAWN: 82,
    chess.KNIGHT: 337,
    chess.BISHOP: 365,
    chess.ROOK: 477,
    chess.QUEEN: 1025,
    chess.KING: 24000,
}

EG_PIECE_VALUES = {
    chess.PAWN: 94,
    chess.KNIGHT: 281,
    chess.BISHOP: 297,
    chess.ROOK: 512,
    chess.QUEEN: 936,
    chess.KING: 24000,
}

# fmt: off
MG_PAWN = [
    0,   0,   0,   0,   0,   0,  0,   0,
    98, 134,  61,  95,  68, 126, 34, -11,
    -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  -5,  12,  17,   6, 10, -25,
    -26,  -4,  -4, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
      0,   0,   0,   0,   0,   0,  0,   0]

EG_PAWN = [
    0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
     94, 100,  85,  67,  56,  53,  82,  84,
     32,  24,  13,   5,  -2,   4,  17,  17,
     13,   9,  -3,  -7,  -7,  -8,   3,  -1,
      4,   7,  -6,   1,   0,  -5,  -1,  -8,
     13,   8,   8,  10,  13,   0,   2,  -7,
      0,   0,   0,   0,   0,   0,   0,   0]

MG_KNIGHT = [
    -167, -89, -34, -49,  61, -97, -15, -107,
     -73, -41,  72,  36,  23,  62,   7,  -17,
     -47,  60,  37,  65,  84, 129,  73,   44,
      -9,  17,  19,  53,  37,  69,  18,   22,
     -13,   4,  16,  13,  28,  19,  21,   -8,
     -23,  -9,  12,  10,  19,  17,  25,  -16,
     -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23]

EG_KNIGHT = [
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64]

MG_BISHOP = [
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -6,  13,  13,  26,  34,  12,  10,   4,
      0,  15,  15,  15,  14,  27,  18,  10,
      4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21]

EG_BISHOP = [
    -14, -21, -11,  -8, -7,  -9, -17, -24,
     -8,  -4,   7, -12, -3, -13,  -4, -14,
      2,  -8,   0,  -1, -2,   6,   0,   4,
     -3,   9,  12,   9, 14,  10,   3,   2,
     -6,   3,  13,  19,  7,  10,  -3,  -9,
    -12,  -3,   8,  10, 13,   3,  -7, -15,
    -14, -18,  -7,  -1,  4,  -9, -15, -27,
    -23,  -9, -23,  -5, -9, -16,  -5, -17]

MG_ROOK = [
     32,  42,  32,  51, 63,  9,  31,  43,
     27,  32,  58,  62, 80, 67,  26,  44,
     -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26]

EG_ROOK = [
    13, 10, 18, 15, 12,  12,   8,   5,
    11, 13, 13, 11, -3,   3,   8,   3,
     7,  7,  7,  5,  4,  -3,  -5,  -3,
     4,  3, 13,  1,  2,   1,  -1,   2,
     3,  5,  8,  4, -5,  -6,  -8, -11,
    -4,  0, -5, -1, -7, -12,  -8, -16,
    -6, -6,  0,  2, -9,  -9, -11,  -3,
    -9,  2,  3, -1, -5, -13,   4, -20]

MG_QUEEN = [
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50]

EG_QUEEN = [
     -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
      3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41]

MG_KING = [
    -65,  23,  16, -15, -56, -34,   2,  13,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
      1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14]

EG_KING = [
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
     10,  17,  23,  15,  20,  45,  44,  13,
     -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43]
# fmt: on

MG_PESTO = {
    chess.PAWN: MG_PAWN,
    chess.KNIGHT: MG_KNIGHT,
    chess.BISHOP: MG_BISHOP,
    chess.ROOK: MG_ROOK,
    chess.QUEEN: MG_QUEEN,
    chess.KING: MG_KING,
}

EG_PESTO = {
    chess.PAWN: EG_PAWN,
    chess.KNIGHT: EG_KNIGHT,
    chess.BISHOP: EG_BISHOP,
    chess.ROOK: EG_ROOK,
    chess.QUEEN: EG_QUEEN,
    chess.KING: EG_KING,
}

############
# Tapered Evaluation: https://www.chessprogramming.org/Tapered_Eval
# Phase values are used to determine on what phase of the game
# we're currently at.
############
PAWN_PHASE = 0
KNIGHT_PHASE = 1
BISHOP_PHASE = 1
ROOK_PHASE = 2
QUEEN_PHASE = 4
TOTAL_PHASE = (
    PAWN_PHASE * 16
    + KNIGHT_PHASE * 4
    + BISHOP_PHASE * 4
    + ROOK_PHASE * 4
    + QUEEN_PHASE * 2
)


def count_pieces(board: chess.Board) -> List[Tuple[int, int]]:
    """
    Counts the number of each piece on the board.

    :param
        board: The board to count the pieces on.
    :return:
        A list of tuples containing the number of pieces of that type
        and their phase value.
    """

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    return [
        (wp, PAWN_PHASE),
        (bp, PAWN_PHASE),
        (wn, KNIGHT_PHASE),
        (bn, KNIGHT_PHASE),
        (wb, BISHOP_PHASE),
        (bb, BISHOP_PHASE),
        (wr, ROOK_PHASE),
        (br, ROOK_PHASE),
        (wq, QUEEN_PHASE),
        (bq, QUEEN_PHASE),
    ]


def get_phase(board: chess.Board) -> float:
    """
    Calculates the phase of the game based on the number of pieces
    on the board.

    :param
        pieces: A list of tuples containing the number of pieces of
        that type and their phase value.
    :return:
        The phase of the game.
    """
    pieces = count_pieces(board)
    phase: float = TOTAL_PHASE

    for piece_count, piece_phase in pieces:
        phase -= piece_count * piece_phase

    phase = (phase * 256 + (TOTAL_PHASE / 2)) / TOTAL_PHASE
    return phase


BOARD_EVALUATION_CACHE = {}
def board_evaluation_cache(fun):

    def inner(board: chess.Board, config: Config):
        key = board.fen()
        if key not in BOARD_EVALUATION_CACHE:
            BOARD_EVALUATION_CACHE[key] = fun(board, config)
        return BOARD_EVALUATION_CACHE[key]
    return inner


@board_evaluation_cache
def board_evaluation(board: chess.Board, config: Config) -> float:
    """
    This functions receives a board and assigns a value to it, it acts as
    an evaluation function of the current state for this game. It returns


    Arguments:
        - board: current board state.

    Returns:
        - total_value(int): integer representing
        current value for this board.
    """
    if config.syzygy_path:
        with chess.syzygy.open_tablebase(config.syzygy_path) as tablebase:
            try:
                eval = tablebase.probe_dtz(board) / 100.0
                return eval
            except (chess.syzygy.MissingTableError, KeyError):
                # Tablebase position not found, continue with evaluation
                pass

    phase = get_phase(board)

    mg = {
        chess.WHITE: 0,
        chess.BLACK: 0,
    }
    eg = {
        chess.WHITE: 0,
        chess.BLACK: 0,
    }

    # loop through all squares and sum their piece values for both sides
    for square in range(64):
        piece = board.piece_at(square)
        if piece is None:
            continue

        if piece.color == chess.WHITE:
            mg[piece.color] += (
                MG_PESTO[piece.piece_type][square ^ 56]
                + MG_PIECE_VALUES[piece.piece_type]
            )
            eg[piece.color] += (
                EG_PESTO[piece.piece_type][square ^ 56]
                + EG_PIECE_VALUES[piece.piece_type]
            )
        if piece.color == chess.BLACK:
            mg[piece.color] += (
                MG_PESTO[piece.piece_type][square]
                + MG_PIECE_VALUES[piece.piece_type]
            )
            eg[piece.color] += (
                EG_PESTO[piece.piece_type][square]
                + EG_PIECE_VALUES[piece.piece_type]
            )

    # calculate board score based on phase
    mg_score = mg[board.turn] - mg[not board.turn]
    eg_score = eg[board.turn] - eg[not board.turn]
    eval = ((mg_score * (256 - phase)) + (eg_score * phase)) / 256

    # print(f"non Tablebase found: {eval}")
    return eval


def evaluate_piece(board: chess.Board, square: chess.Square, phase: float) -> float:
    """
    Evaluates a piece on a given square.

    Arguments:
        - board: current board state.
        - square: square to evaluate.
        - phase: current phase of the game.

    Returns:
        - value(float): float representing
        current value for this piece on this square.
    """
    mg_score = 0
    eg_score = 0

    # get mid and end game score for single piece
    piece = board.piece_at(square)
    if piece is not None:
        if piece.color == chess.WHITE:
            mg_score += (
                MG_PESTO[piece.piece_type][square ^ 56]
                + MG_PIECE_VALUES[piece.piece_type]
            )
            eg_score += (
                EG_PESTO[piece.piece_type][square ^ 56]
                + EG_PIECE_VALUES[piece.piece_type]
            )
        if piece.color == chess.BLACK:
            mg_score += (
                MG_PESTO[piece.piece_type][square] + MG_PIECE_VALUES[piece.piece_type]
            )
            eg_score += (
                EG_PESTO[piece.piece_type][square] + EG_PIECE_VALUES[piece.piece_type]
            )

    # evaluate piece value based on phase
    eval = ((mg_score * (256 - phase)) + (eg_score * phase)) / 256
    return eval


def evaluate_capture(board: chess.Board, move: chess.Move, phase: float) -> float:
    """
    Evaluates a capture move based phase of the game.

    Arguments:
        - board: current board state.
        - move: move to evaluate.
        - phase: current phase of the game.

    Returns:
        - value(float): float representing
        value for this capture.
    """
    mg_score = 0
    eg_score = 0

    # en passant score
    if board.is_en_passant(move):
        return 0

    capturing_piece = board.piece_at(move.from_square).piece_type  # type: ignore
    captured_piece = board.piece_at(move.to_square).piece_type  # type: ignore

    # get mid and end game difference of scores between captured
    # and capturing piece
    if capturing_piece is not None and captured_piece is not None:
        mg_score += MG_PIECE_VALUES[captured_piece] - MG_PIECE_VALUES[capturing_piece]
        eg_score += EG_PIECE_VALUES[captured_piece] - EG_PIECE_VALUES[capturing_piece]

    # evaluate capture based on game's phase
    eval = ((mg_score * (256 - phase)) + (eg_score * phase)) / 256
    return eval
