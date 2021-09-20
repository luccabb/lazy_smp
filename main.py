from flask import request
from flask_cors import CORS, cross_origin
from flask import Flask
import json
import chess
import multiprocessing as mp
import functools
import copy
import random

PIECE_VALUES = {
    'q': 27,
    'p': 2,
    'n': 8,
    'b': 13,
    'r': 14,
    'k': 1000,
}
CENTER_ROWS = [3, 4]
CENTER_COLUMNS = [0,1,2,3,4,5,6,7]
QUEEN_START = (7, 3)
KNIGHT_ROW = 7
LEFT_KNIGHT_COL = 1
RIGHT_KNIGHT_COL = 6
BISHOP_ROW = 7
LEFT_BISHOP_ROW = 2
RIGHT_BISHOP_ROW = 5
CORNERS = [(0,0), (0,1), (1,0), (1,1), (0,7), (0,6), (1,7), (1,6), (6,6), (6,7), (7,6), (7,7), (6,0), (6,1), (7,1), (7,0)]

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADER'] = 'Content-Type'

def count_pieces(board):
    black_pieces, white_pieces = 0, 0

    for row in range(0,8):
        for col in range(0,8):
            squareIndex=row*8+col
            square=chess.SQUARES[squareIndex]
            piece = board.piece_at(square)
            if piece:
                if piece.color == chess.BLACK:
                    black_pieces += 1
                else:
                    white_pieces += 1
    return black_pieces, white_pieces

def board_value(board, player):
    # assign a value to the board (evaluation function)
    total_value = 0
    black_pieces = 0
    white_pieces = 0

    black_pieces, white_pieces = count_pieces(board)
    
    for row in range(8):
      for col in range(8):
        square_index = row*8+col
        square = chess.SQUARES[square_index]
        piece = board.piece_at(square)

        if piece:

            piece_color = piece.color

            if piece.symbol().lower() in PIECE_VALUES:
                #  adding to totalValue the value coming from black pieces.
                #  When the black is evaluating it will try to find the highest possible totalValue
                #  in this case meaning that it has more black pieces in the table and less white pieces
                if piece_color == chess.BLACK:
                    total_value += 1
                else:
                    total_value -= 1
            
            if piece.symbol().lower() == 'p':
                pawn_in_col = 0

                # count pawns in column
                for j in range(8):
                    square_index_helper = j*8+col
                    square_helper = chess.SQUARES[square_index_helper]
                    piece_helper = board.piece_at(square_helper)
                    if piece_helper and piece_helper.symbol().lower() == 'p' and piece_helper.color == piece_color:
                        pawn_in_col += 1
                
                if pawn_in_col >= 2:
                    if piece_color == chess.BLACK:
                        total_value -= 0.5*pawn_in_col
                    else:
                        total_value += 0.5*pawn_in_col
            
            # if we are in the beginning of the game, we want to have a few different heuristics
            if white_pieces + black_pieces >= 27:
                # removing points for moving queen too early in the game
                if piece.symbol().lower() == 'q' and (row, col) != QUEEN_START:
                    if piece_color == chess.BLACK:
                        total_value -= 6
                    else:
                        total_value += 6

                # points for moving knight early in the game
                if piece.symbol().lower() == 'n' and (row != KNIGHT_ROW or (col != LEFT_KNIGHT_COL or col != RIGHT_KNIGHT_COL)):
                    if piece_color == chess.BLACK:
                        total_value += 3
                    else:
                        total_value -= 3

                # points for moving bishop early in the game
                if piece.symbol().lower() == 'b' and (row != BISHOP_ROW or (col != LEFT_BISHOP_ROW or col != RIGHT_BISHOP_ROW)):
                    if piece_color == chess.BLACK:
                        total_value += 3
                    else:
                        total_value -= 3

                # points for dominating the middle squares
                # 4 squares in the center of the board
                if row in CENTER_ROWS and col in CENTER_ROWS:
                    if piece_color == chess.BLACK:
                        total_value += 0.07
                    else:
                        total_value -= 0.07

                # points for dominating the middle rows
                if row in CENTER_ROWS and col in CENTER_COLUMNS:
                    if piece_color == chess.BLACK:
                        total_value += 0.06
                    else:
                        total_value -= 0.06

            # end game heuristics
            if white_pieces <= 6:
                if piece.symbol().lower() == 'k':
                    if (row, col) in CORNERS:
                        if piece_color == chess.WHITE:
                            total_value += 9
                        else:
                            total_value -= 9

            elif black_pieces <= 6:
                if piece.symbol().lower() == 'k':
                    if (row, col) in CORNERS:
                        if piece_color == chess.BLACK:
                            total_value -= 9
                        else:
                            total_value += 9

    # this function will be called for both players so we need to adjust its output accordingly
    return total_value if player else -total_value

def get_move_score(board, depth, player: bool):
    # recursion base case
    if (depth == 0):
        # evaluate this board
        value = board_value(board, player)
        return value, None

    best_move = None
    # to ensure that we make changes to a different game object
    cloned_board = copy.deepcopy(board)

    # initializing bestMoveValue found depending on the player
    if player:
        best_move_value = float("-inf")
    else:
        best_move_value = float("inf")

    alpha = float("-inf")
    beta = float("inf")
    for move in board.legal_moves:
        cloned_board.push(move) # Make the move

        if cloned_board.can_claim_threefold_repetition():
            cloned_board.pop() # unmake the last move
            continue

        value = get_move_score(cloned_board, depth-1, not player)[0]

        if player:
            # Look for moves that maximize position, (AI moves)
            if value > best_move_value:
                # if it was the highest evaluation function move so far, we make this move
                best_move_value = value
                best_move = move
            # setting alpha variable to do prunning later on
            alpha = max(alpha,  value)
        else:
            # Look for best moves that minimize position, (Human moves)
            if value < best_move_value:
                # we assume human is making the best move for himself
                best_move_value = value
                best_move = move
            # setting beta variable to do prunning
            beta = min(beta, value)

        cloned_board.pop() # undo fake move

        # alpha beta prunning when we already found a solution that is at least as good as the current one
        # those branches won't be able to influence the final decision so we don't need to waste time analyzing them
        if beta <= alpha:
            break

    if not best_move:
        if board.legal_moves:
            best_move = random.choice([move for move in board.legal_moves])
        else:
            best_move = (None, None)

    # if it returned no best move, we make a random one
    return [best_move_value, best_move]

def get_main_move_score(board, move, depth, player: bool):
    # to ensure that we make changes to a different game object
    cloned_board = copy.deepcopy(board)

    cloned_board.push(move) # Make the move

    if cloned_board.can_claim_threefold_repetition():
        cloned_board.pop() # unmake the last move
        return 0, None

    value, best_move = get_move_score(cloned_board, depth-1, not player)

    cloned_board.pop() # unmake the last move

    return value, move

@app.route('/')
@cross_origin()
def hello_world():
    fen = request.args.get('fen')
    board = chess.Board(fen)
    
    nprocs = mp.cpu_count()
    pool = mp.Pool(processes=nprocs)
    print(nprocs, 'start')
    print([move for move in board.legal_moves])
    arguments = [(board, move, 2, True) for move in board.legal_moves]
    result = pool.starmap(get_main_move_score, arguments)
    result = sorted(result, key = lambda a: a[0])
    print(result)
    return {
        'statusCode': 200,
        'body': {'move': result[-1][1].uci()},
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
    }

    return "Hello World!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

