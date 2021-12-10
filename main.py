from flask import request
from flask_cors import CORS, cross_origin
from flask import Flask
import chess
import random
import time
import helper
from typing import Tuple, Dict, Union, Any


# Evaluation function constants
MOVES = []
PIECE_VALUES = {
	'p': 2,
	'n': 8,
	'b': 13,
	'r': 14,
	'q': 27,
	'k': 1000,
}
CENTER_ROWS = [3, 4]
CENTER_COLUMNS = [0, 1, 2, 3, 4, 5, 6, 7]
QUEEN_START = [(7, 3), (0, 3)]
KNIGHT_ROW = [0, 7]
LEFT_KNIGHT_COL = 1
RIGHT_KNIGHT_COL = 6
BISHOP_ROW = [0, 7]
LEFT_BISHOP_ROW = 2
RIGHT_BISHOP_ROW = 5
CORNERS = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 7), (0, 6), (1, 7), (1, 6),
			(6, 6), (6, 7), (7, 6), (7, 7), (6, 0), (6, 1), (7, 1), (7, 0)]

# Search constants
R = 2
COUNTER = 0

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADER'] = 'Content-Type'


def count_pieces(board: chess.Board) -> Tuple[int]:
	"""
	Receives a board state and counts the number of pieces for each player in it.

	Arguments:
		- board: current board state.

	Returns:
		- black_pieces, white_pieces(Tuple[int]): Tuple of
		integers representing count of pieces for each player.
	"""
	black_pieces, white_pieces = 0, 0

	for row in range(0, 8):
		for col in range(0, 8):
			squareIndex = row*8+col
			square = chess.SQUARES[squareIndex]
			piece = board.piece_at(square)
			if piece:
				if piece.color == chess.BLACK:
					black_pieces += 1
				else:
					white_pieces += 1
	return black_pieces, white_pieces


def board_value(board: chess.Board) -> float:
	"""
	This functions receives a board and assigns a value to it, it acts as
	an evaluation function of the current state for this game. It returns


	Arguments:
		- board: current board state.

	Returns:
		- total_value(int): integer representing
		current value for this board.
	"""
	total_value = 0

	black_pieces, white_pieces = count_pieces(board)

	for row in range(8):
		for col in range(8):

			square_index = row*8+col
			square = chess.SQUARES[square_index]
			piece = board.piece_at(square)

			if piece:

				piece_color = piece.color

				#  adding to totalValue the value coming from black pieces.
				#  When the black is evaluating it will try to find the highest possible totalValue
				#  in this case meaning that it has more black pieces in the table and less white pieces
				if piece.symbol().lower() in PIECE_VALUES:
					if piece_color == chess.BLACK:
						total_value += PIECE_VALUES[piece.symbol().lower()]
					else:
						total_value -= PIECE_VALUES[piece.symbol().lower()]

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
					if piece.symbol().lower() == 'q' and (row, col) not in QUEEN_START:
						if piece_color == chess.BLACK:
							total_value -= 6
						else:
							total_value += 6

					# points for moving knight early in the game
					if piece.symbol().lower() == 'n' and (row not in KNIGHT_ROW and (col != LEFT_KNIGHT_COL or col != RIGHT_KNIGHT_COL)):
						if piece_color == chess.BLACK:
							total_value += 3
						else:
							total_value -= 3

					# points for moving bishop early in the game
					# False
					if piece.symbol().lower() == 'b' and (row not in BISHOP_ROW and (col != LEFT_BISHOP_ROW or col != RIGHT_BISHOP_ROW)):
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
					elif row in CENTER_ROWS and col in CENTER_COLUMNS:
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

	return round(total_value, 2)


def get_move_score(
	board: chess.Board,
	depth: int,
	player: bool,
	null_move: bool,
	alpha: float = float("-inf"),
	beta: float = float("inf")) -> Tuple[Union[int, chess.Move]]:
	"""
	This functions receives a board, depth and a player; and it returns
	the best move for the current board based on how many depths we're looking ahead
	and which player is playing. Alpha and beta are used to prune the search tree.
	Alpha represents the best score for the maximizing player (best choice (highest value)  we've found
	along the path for max) and beta represents the best score for the minimizing player
	(best choice (lowest value) we've found along the path for min). When Alpha is higher
	than or equal to Beta, we can prune the search  tree; because it means that the
	maximizing player won't find a better move in this branch.

	OBS:
		- We only need to evaluate the value for leaf nodes because they are our final states
		of the board and therefore we need to use their values to base our decision of what is
		the best move.

	Arguments:
		- board: chess board state
		- depth: how many depths we want to calculate for this board
		- player: player that is currently moving pieces. True for black, False for white.

	Returns:
		- best_move_value, best_move: returns best move that it found and its value.
	"""
	global COUNTER
	COUNTER += 1
	# recursion base case
	if depth <= 0:
		# evaluate current board
		value = board_value(board)
		return value, None, alpha

	# null move heuristic
	# alpha = get_move_score(board, depth-1 - R, not player, beta, beta-1)[2]
	# if alpha >= beta:
	# 	value = board_value(board)
	# 	return value, None, alpha

	best_move = None

	# initializing bestMoveValue found depending on the player
	if player:
		best_move_value = float("-inf")
	else:
		best_move_value = float("inf")

	for move in board.legal_moves:
		# alpha beta prunning when we already found a solution that is at least as good as the current one
		# those branches won't be able to influence the final decision so we don't need to waste time analyzing them
		if alpha >= beta:
			break

		board.push(move)  # Make the move

		if board.can_claim_threefold_repetition():
			board.pop()  # unmake the last move
			continue

		value, _, _ = get_move_score(board, depth-1, not player, True, alpha, beta)

		if player:
			# Look for moves that maximize position, (AI moves)
			if value > best_move_value:
				# if it was the highest evaluation function move so far, we make this move
				best_move_value = value
				best_move = move
			# setting alpha variable to do prunning
			alpha = max(alpha, value)
		else:
			# Look for best moves that minimize position, (Human moves)
			if value < best_move_value:
				# we assume human is making the best move for himself
				best_move_value = value
				best_move = move
			# setting beta variable to do prunning
			beta = min(beta, value)

		# take move back
		board.pop()

	# if it returned no best move, we make a random one
	if not best_move:
		best_move = random.choice([move for move in board.legal_moves])

	return best_move_value, best_move, alpha


def quiescence_search(board: chess.Board, player: int, alpha: float, beta: float):
	stand_pat = player * board_value(board)
	if(stand_pat >= beta):
		return beta

	if(alpha < stand_pat):
		alpha = stand_pat

	for move in board.legal_moves:
		if board.is_capture(move):
			board.push(move)
			score = -quiescence_search(board, -player, -beta, -alpha)
			board.pop()

			if(score >= beta):
				return beta
			
			if(score > alpha):
				alpha = score  
	return alpha


def format_response(best_move: str) -> Dict[str, Any]:
	return {
		'statusCode': 200,
		'body': {'move': best_move},
		'headers': {
			'Access-Control-Allow-Headers': 'Content-Type',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,GET'
		},
	}


@app.route('/')
@cross_origin()
def main_search() -> Dict[str, Any]:
	st = time.time()
	fen = request.args.get('fen')
	board = chess.Board(fen)

	# ALGORITHM_NAME =  "alpha_beta"
	# ALGORITHM_NAME = "parallel_alpha_beta_layer_1"
	ALGORITHM_NAME = "parallel_alpha_beta_layer_2"
	# ALGORITHM_NAME = "lazy_smp"

	engine = helper.get_implementation(ALGORITHM_NAME)

	depth = 7
	player = 1
	null_move = True

	best_move = engine(board, depth, player, null_move)
	end = time.time()
	print((end - st) * 1000)
	return format_response(best_move)


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)
