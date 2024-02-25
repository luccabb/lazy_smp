import sys

from chess import STARTING_FEN, Board, polyglot

from helper import get_engine
from config import Config
import chess
from typing import List
import time

# UCI based on Sunfish Engine: https://github.com/thomasahle/sunfish/blob/master/uci.py

def count_pieces(board: chess.Board) -> List[int]:
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
        wp,
        bp,
        wn,
        bn,
        wb,
        bb,
        wr,
        br,
        wq,
        bq,
    ]

def main(config: Config):
    """
    Start the command line user interface (UCI based).
    """
    # init board and engine
    board = Board()
    engine = get_engine(config)

    # keep listening to UCI commands
    while True:
        # get command from stdin
        uci_command = input().strip()
        uci_parameters = uci_command.split(" ")

        if uci_command == "quit":
            sys.exit()

        elif uci_command == "uci":
            # engine details
            print("id name Moonfish")
            print("id author luccabb")
            print("uciok")

        elif uci_command == "isready":
            # engine ready to receive commands
            print("readyok")

        elif uci_command == "ucinewgame":
            # start new game
            board = Board()

        elif uci_command.startswith("position"):
            moves_idx = uci_command.find("moves")

            # get moves from UCI command
            if moves_idx >= 0:
                moveslist = uci_command[moves_idx:].split()[1:]
            else:
                moveslist = []

            # get FEN from uci command
            if uci_parameters[1] == "fen":
                if moves_idx >= 0:
                    fenpart = uci_command[:moves_idx]
                    _, _, fen = fenpart.split(" ", 2)
                else:
                    fen = " ".join(uci_parameters[2:])

            elif uci_parameters[1] == "startpos":
                fen = STARTING_FEN
            else:
                raise SyntaxError("UCI Syntax error.")

            # start board and make moves
            board = Board(fen)
            for move in moveslist:
                board.push_uci(move)

        elif uci_command.startswith("go"):

            # try using cerebellum opening book: https://zipproth.de/Brainfish/download/
            # if it fails we search on our engine. The first (12-20) moves should be
            # available in the opening book, so our engine starts playing after that.
            st = time.time()
            try:
                best_move = (
                    polyglot.MemoryMappedReader("opening_book/cerebellum.bin")
                    .find(board)
                    .move
                    .uci()
                )
            except:
                best_move = engine.search_move(board)
            print(f"Time: {time.time() - st}")
            print(f"bestmove {best_move}")
