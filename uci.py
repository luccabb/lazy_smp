import sys

from chess import STARTING_FEN, Board

from constants import ALGORITHM_NAME, NEGAMAX_DEPTH, NULL_MOVE
from helper import get_engine

# UCI based on Sunfish Engine: https://github.com/thomasahle/sunfish/blob/master/uci.py


def start():
    """
    Start the command line user interface (UCI based).
    """
    # init board and engine
    board = Board()
    engine = get_engine(ALGORITHM_NAME)
    
    # keep listening to UCI commands
    while True:
        # get command from stdin
        uci_command = input().strip()
        uci_parameters = uci_command.split(" ")

        if uci_command == "quit":
            sys.exit()

        elif uci_command == "uci":
            # engine details
            print('id name Moonfish')
            print('id author Lucca B')
            print("uciok")
        
        elif uci_command == "isready":
            # engine ready to receive commands
            print("readyok")

        elif uci_command == "ucinewgame":
            # start new game
            board = Board()
        
        elif uci_command.startswith("position"):
            moves_idx = uci_command.find('moves')

            # get moves from UCI command
            if moves_idx >= 0:
                moveslist = uci_command[moves_idx:].split()[1:]
            else:
                moveslist = []
            
            # get FEN from uci command
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

            # start board and make moves
            board = Board(fen)
            for move in moveslist:
                board.push_uci(move)
        
        elif uci_command.startswith("go"):
            # search and print best move
            best_move = engine.search_move(board, NEGAMAX_DEPTH, NULL_MOVE)
            print(f"bestmove {best_move}")

