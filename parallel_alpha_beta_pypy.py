#!/usr/bin/env pypy

import chess
import multiprocessing as mp
import psqt_pypy
import main_pypy
import random
from collections import defaultdict
import copy
import move_ordering_pypy

# Search constants
DEPTHS = 2


def negamax(
	board, 
	depth, 
	player, 
	null_move,
	alpha = float("-inf"), 
	beta = float("inf")):
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

	# recursion base case
	if depth <= 0:
		# evaluate current board
		# value = quiescence_search(board, player, alpha, beta)
		score = player * psqt_pypy.board_value_piece_square(board)
		return score, None

	# null move prunning
	if null_move and depth >= (main_pypy.R+1) and not board.is_check():
		board.push(chess.Move.null())
		score = -negamax(board, depth -1 - main_pypy.R, -player, False, -beta, -beta+1)[0]
		board.pop()
		if score >= beta:
			return beta, None

	best_move = None

	# initializing best_score
	best_score = float("-inf")
	
	# for move in board.legal_moves:
	for move in move_ordering_pypy.organize_moves(board):
		# make the move
		board.push(move)

		# if threefold repetition we do not analyze this position
		if board.can_claim_threefold_repetition():
			board.pop()  
			continue

		score = -negamax(board, depth-1, -player, null_move, -beta, -alpha)[0]

		# take move back
		board.pop()

		# beta-cutoff
		if score >= beta:
			return score, move

		# update best move
		if score > best_score:
			best_score = score
			best_move = move
		
		# setting alpha variable to do pruning
		alpha = max(alpha, score)

		# alpha beta pruning when we already found a solution that is at least as good as the current one
		# those branches won't be able to influence the final decision so we don't need to waste time analyzing them
		if alpha >= beta:
			break

	# if it returned no best move, we make a random one
	if not best_move:
		if board.legal_moves:
			best_move = random.choice([move for move in board.legal_moves])
		else:
			best_move = None
	
	return best_score, best_move


def get_black_pieces_best_move(board, move, depth, player, null_move):
	
	# make move
	board.push(move)

	# check threefold repetition
	if board.can_claim_threefold_repetition():
		board.pop()  # unmake the last move
		return 0, None

	value, _ = negamax(board, depth-1, player, null_move)

	# remove move
	board.pop()

	return board, value, move


def alpha_beta(board, depth, player, null_move):
	return negamax(board, depth, player, null_move)[1].uci()


def parallel_alpha_beta_layer_2(board, depth, player, null_move):
	# search constants
	START_LAYER = 2
	depth = depth - START_LAYER
	layer_1_pointer = {}

	nprocs = mp.cpu_count()
	pool = mp.Pool(processes=nprocs)

	layer_1_moves = board.legal_moves
	start_layer_moves = []  # list of tuples containing (board, move)

	# building START_LAYER pointers to layer_1
	# once we find the best move at START_LAYER
	# we need to be able to point to the layer 1
	# movement that generates the best move at START_LAYER
	while START_LAYER:
		for move_1 in layer_1_moves:
			board.push(move_1)
			if board.is_checkmate() or board.is_stalemate():
				return move_1
			for move_2 in board.legal_moves:
				layer_1_pointer[(
					copy.copy(board.fen()),
					move_2.uci())] = move_1
				start_layer_moves.append((copy.copy(board), move_2))
			board.pop()
		START_LAYER -= 1

	# sending all possible nodes from start layer to a different processor
	# TODO: call negamax directly instead of get_black_pieces_best_move.
	arguments = [(board, move, depth, player, null_move)
				 for board, move in start_layer_moves]
	start_layer_result = pool.starmap(get_black_pieces_best_move, arguments)

	# organizing all the possible achievable values/move
	# per board.
	layer_1_boards_with_moves = defaultdict(list)
	for board, value, move in start_layer_result:
		board = copy.copy(board)
		layer_1_boards_with_moves[(board.fen())].append((value, move))

	# for each node in the first layer we need to find the lowest node
	# in the second layer (white pieces moving we need to minimize the value)
	# Then we get the best move for the first layer by maximizing the values
	layer_1_nodes = []
	for board in layer_1_boards_with_moves:
		lowest_node = (board, layer_1_boards_with_moves[board][0][0], layer_1_boards_with_moves[board][0][1])
		for layer_1_value, move in layer_1_boards_with_moves[board][1:]:
			if layer_1_value < lowest_node[1]:
				lowest_node = (board, layer_1_value, move)
		layer_1_nodes.append(lowest_node)

	layer_1_nodes.sort(key=lambda a: a[1])
	best_board, best_move = layer_1_nodes[-1][0], layer_1_nodes[-1][2].uci()
	best_move = layer_1_pointer[best_board, best_move].uci()

	return best_move


def parallel_alpha_beta_layer_1(board, depth, player, null_move):
	# creating pool of processes
	nprocs = mp.cpu_count()
	pool = mp.Pool(processes=nprocs)

	# creating list of moves at layer 1
	arguments = [(board, move, depth, player, null_move) for move in board.legal_moves]
	# executing all the moves at layer 1 in parallel
	# starmap blocks until all processes are done
	result = pool.starmap(get_black_pieces_best_move, arguments)

	# sorting output and getting best move
	best_move = sorted(result, key = lambda a: a[1])[-1][2].uci()

	return best_move