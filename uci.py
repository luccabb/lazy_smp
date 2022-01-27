from chess import Board, STARTING_FEN
import sys
from helper import get_engine
from constants import ALGORITHM_NAME, NULL_MOVE, NEGAMAX_DEPTH
# UCI based on Sunfish Engine: https://github.com/thomasahle/sunfish/blob/master/uci.py


def start():
    """
    Start the command line user interface (UCI based).
    """
    board = Board()
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
            board = Board()
        
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
                fen = STARTING_FEN

            else:
                raise SyntaxError("UCI Syntax error.")

            board = Board(fen)

            for move in moveslist:
                board.push_uci(move)
        
        elif uci_command.startswith("go"):
            best_move = engine(board, NEGAMAX_DEPTH, NULL_MOVE)
                
            print(f"bestmove {best_move}")

