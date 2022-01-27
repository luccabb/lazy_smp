import chess
import random
from psqt import get_phase, evaluate_piece, evaluate_capture

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
	# moves = [l for l in board.legal_moves]
	# random.shuffle(moves)
	# return moves
	non_captures = []
	captures = []

	for move in board.legal_moves:
		if board.is_capture(move):
			captures.append(move)
		else:
			non_captures.append(move)
	
	random.shuffle(captures) 
	random.shuffle(non_captures)
	return captures + non_captures


def organize_moves_quiescence(board: chess.Board):
	"""
	This function receives a board and it returns a list of all the
	possible moves for the current player, sorted by importance.

	Arguments:
		- board: chess board state

	Returns:
		- moves: list of all the possible moves for the current player sorted based on importance.
	"""
	phase = get_phase(board)
	captures = filter(lambda move: board.is_zeroing(move) or board.gives_check(move), board.legal_moves)
	moves = sorted(captures, key=lambda move: mvv_lva(board, move, phase), reverse=(True if board.turn == chess.BLACK else False))
	return moves


def mvv_lva(board: chess.Board, move: chess.Move, phase: float):
	move_value = 0

	# evaluating position 
	from_value = evaluate_piece(board, move.from_square, phase)
	to_value = evaluate_piece(board, move.to_square, phase)

	move_value += to_value - from_value

	# evaluating capture
	if board.is_capture(move):
		move_value += evaluate_capture(board, move, phase)

	return -move_value if board.turn else move_value