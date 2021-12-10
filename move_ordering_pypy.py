import random

def organize_moves(board):
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