from flask import request
from flask_cors import CORS, cross_origin
from flask import Flask
import json
import chess
import multiprocessing as mp
import functools
import copy
import random
import time
import psqt
from typing import Tuple, Dict, Union, Any
from collections import defaultdict, deque

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
START_LAYER = 2
DEPTHS = 2
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
		if board.legal_moves:
			best_move = random.choice([move for move in board.legal_moves])
		else:
			best_move = (None, None)

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


def organize_moves(board: chess.Board):
	"""
	This function receives a board and it returns a list of all the
	possible moves for the current player, sorted by importance.
	Right now we are only sending the moves that are capturing pieces
	at the starting positions in our array (so we can prune more and earlier).

	Arguments:
		- board: chess board state

	Returns:
		- legal_moves: list of all the possible moves for the current player.
	"""
	org_moves = deque()
	for move in board.legal_moves:
		if board.is_capture(move):
			org_moves.appendleft(move)
		else:
			org_moves.append(move)
	return list(org_moves)


def negamax(
	board: chess.Board, 
	depth: int, 
	player: int, 
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
		- player: player that is currently moving pieces. 1 for AI (max), -1 for human (min).

	Returns:
		- best_score, best_move: returns best move that it found and its value.
	"""
	global COUNTER
	COUNTER += 1

	# recursion base case
	if depth == 0:
		# evaluate current board
		# value = quiescence_search(board, player, alpha, beta)
		# return value, None
		# if not board.turn:
		# 	score = board_value(board)
		# else: 
		# 	score = -board_value(board)
		# score = player * board_value(board)
		score = player * psqt.board_value_piece_square(board)
		return score, None

	# null move prunning
	if null_move and depth >= (R+1) and not board.is_check():
		board.push(chess.Move.null())
		score = -negamax(board, depth -1 - R, -player, False, -beta, -beta+1)[0]
		board.pop()
		if score >= beta:
			return beta, None

	best_move = None

	# initializing best_score
	best_score = float("-inf")
	
	# for move in board.legal_moves:
	for move in organize_moves(board):
		# Make the move
		board.push(move)

		# # if threefold repetition, we don't want to evaluate this move
		# if board.can_claim_threefold_repetition():
		# 	board.pop()  
		# 	continue

		score, _ = negamax(board, depth-1, -player, null_move, -beta, -alpha)
		score = -score

		# take move back
		board.pop()

		if score >= beta:
			return score, move

		# Look for moves that maximize position, (AI moves)
		if score > best_score:
			# if it was the highest evaluation function move so far, we make this move
			best_score = score
			best_move = move
		
		# setting alpha variable to do prunning
		alpha = max(alpha, score)

		# alpha beta prunning when we already found a solution that is at least as good as the current one
		# those branches won't be able to influence the final decision so we don't need to waste time analyzing them
		if alpha >= beta:
			break

	# if it returned no best move, we make a random one
	if not best_move:
		if board.legal_moves:
			best_move = random.choice([move for move in board.legal_moves])
		else:
			best_move = (None, None)
	
	return best_score, best_move


def get_black_pieces_best_move(board: chess.Board, move, depth: int) -> Tuple[Union[int, chess.Move]]:
	board.push(move)
	if board.can_claim_threefold_repetition():
		board.pop()  # unmake the last move
		return 0, None

	# value, _, _ = get_move_score(board, depth-1, True, True)
	value, _ = negamax(board, depth-1, 1, True)

	board.pop()
	return board, value, move


def get_black_pieces_best_move_1(board: chess.Board, move, depth: int) -> Tuple[Union[int, chess.Move]]:

	# initializing best_score found depending on the player
	best_move = None
	best_score = float("-inf")

	board.push(move)
	if board.can_claim_threefold_repetition():
		board.pop()  # unmake the last move
		return 0, None

	# value, _, _ = get_move_score(board, depth-1, True, True)
	value, _ = negamax(board, depth-1, 1, True)

	board.pop()
	return board, value, move


@app.route('/')
@cross_origin()
def main_search() -> Dict[str, Any]:
	global COUNTER

	fen = request.args.get('fen')
	START_LAYER = 2

	board = chess.Board(fen)
	layer_1_pointer = {}

	nprocs = mp.cpu_count()
	pool = mp.Pool(processes=nprocs)

	print(nprocs, 'start')
	st = time.time()

	layer_1_moves = board.legal_moves
	start_layer_moves = []  # list of tuples containing (board, move)

	while START_LAYER:
		for move_1 in layer_1_moves:
			board.push(move_1)
			if board.is_checkmate() or board.is_stalemate():
				return {
					'statusCode': 200,
					'body': {'move': move_1.uci()},
					'headers': {
						'Access-Control-Allow-Headers': 'Content-Type',
						'Access-Control-Allow-Origin': '*',
						'Access-Control-Allow-Methods': 'OPTIONS,GET'
					},
				}
			for move_2 in board.legal_moves:
				layer_1_pointer[(
					copy.copy(board.fen()), 
					move_2.uci())] = move_1.uci()
				start_layer_moves.append((copy.copy(board), move_2))
			board.pop()
		START_LAYER -= 1
	
	# TODO: implement transposition table

	arguments = [(board, move, DEPTHS)
				 for board, move in start_layer_moves]
	layer_2_result = pool.starmap(get_black_pieces_best_move, arguments)

	layer_1_boards_with_moves = defaultdict(list)
	for board, value, move in layer_2_result:
		board = copy.copy(board)

		layer_1_boards_with_moves[(board.fen())].append((value, move))

	# for each node in the first layer we need to find the lowest node
	# in the second layer (white pieces moving we need to minimize the value)
	# Then we get the best move for the first layer by maximizing the values
	layer_1_nodes = []
	for board in layer_1_boards_with_moves:
		lowest_node = (board, *layer_1_boards_with_moves[board][0])
		for layer_1_value, move in layer_1_boards_with_moves[board][1:]:
			if layer_1_value < lowest_node[1]:
				lowest_node = (board, layer_1_value, move)
		layer_1_nodes.append(lowest_node)

	layer_1_nodes.sort(key=lambda a: a[1])
	best_move = layer_1_pointer[layer_1_nodes[-1][0], layer_1_nodes[-1][2].uci()]
	end = time.time()
	print(end-st)
	print('counter>', COUNTER)

	return {
		'statusCode': 200,
		'body': {'move': best_move},
		'headers': {
			'Access-Control-Allow-Headers': 'Content-Type',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,GET'
		},
	}


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)