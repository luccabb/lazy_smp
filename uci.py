import chess
import argparse
import helper
# UCI based on Sunfish Engine: https://github.com/thomasahle/sunfish/blob/master/uci.py

# Constants
# ALGORITHM_NAME =  "alpha_beta"
# ALGORITHM_NAME = "parallel_alpha_beta_layer_1"
ALGORITHM_NAME = "parallel_alpha_beta_layer_2"
# ALGORITHM_NAME = "lazy_smp"
NULL_MOVE = True

def start():
    """
    Start the command line user interface.
    """
    while True:
        command = input()

        if command == "quit":
            break

        elif command == "uci":
            print('id name Moonfish')
            print('id author Lucca B')
            print("uciok")
        
        elif command == "isready":
            print("readyok")

        elif command == "ucinewgame":
            # start new game
            board = chess.Board()
        
        elif command.startswith("position"):
            params = command.split(" ")
            idx = command.find('moves')

            if idx >= 0:
                moveslist = command[idx:].split()[1:]
            else:
                moveslist = []

            if params[1] == 'fen':
                if idx >= 0:
                    fenpart = command[:idx]
                else:
                    fenpart = command

                _, _, fen = fenpart.split(' ', 2)

            elif params[1] == 'startpos':
                fen = chess.STARTING_FEN

            else:
                raise SyntaxError("UCI Syntax error.")

            board = chess.Board(fen)

            for move in moveslist:
                board.push_san(move)
        
        elif command == "go":
            engine = helper.get_implementation(ALGORITHM_NAME)
            params = command.split(" ")

            if "depth" in params:
                depth = int(params[params.index("depth") + 1])
            else:
                depth = 3
            
            best_move = engine(board, depth, NULL_MOVE)
            
            print(f"bestmove {best_move}")
