import chess
from helper import get_engine
import chess.polyglot
import sys
# UCI based on Sunfish Engine: https://github.com/thomasahle/sunfish/blob/master/uci.py

# Constants
# ALGORITHM_NAME =  "alpha_beta"
ALGORITHM_NAME = "parallel_alpha_beta_layer_2"
# ALGORITHM_NAME = "lazy_smp"
NULL_MOVE = True
DEPTH = 3


def start():
    """
    Start the command line user interface (UCI based).
    """
    board = chess.Board()
    engine = get_engine(ALGORITHM_NAME)
    
    # keep listening to UCI commands
    while True:
        uci_command = input().strip()
        uci_parameters = uci_command.split(" ")

        if uci_command == "quit":
            sys.exit()

        elif uci_command == "uci":
            print('id name Moonfish')
            print('id author Lucca B')
            print("uciok")
        
        elif uci_command == "isready":
            print("readyok")

        elif uci_command == "ucinewgame":
            # start new game
            board = chess.Board()
        
        elif uci_command.startswith("position"):
            moves_idx = uci_command.find('moves')

            if moves_idx >= 0:
                moveslist = uci_command[moves_idx:].split()[1:]
            else:
                moveslist = []

            if uci_parameters[1] == 'fen':
                if moves_idx >= 0:
                    fenpart = uci_command[:moves_idx]
                else:
                    fenpart = uci_command

                _, _, fen = fenpart.split(' ', 2)

            elif uci_parameters[1] == 'startpos':
                fen = chess.STARTING_FEN

            else:
                raise SyntaxError("UCI Syntax error.")

            board = chess.Board(fen)

            for move in moveslist:
                board.push_uci(move)
        
        elif uci_command.startswith("go"):
            best_move = engine(board, DEPTH, NULL_MOVE)
                
            print(f"bestmove {best_move}")

