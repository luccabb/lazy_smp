#!/usr/bin/env pypy

import chess
import multiprocessing as mp
import main_pypy
import psqt_pypy
import random
import move_ordering_pypy


def negamax_smp(
	board, 
	depth, 
	player, 
	null_move,
	shared_hash_table,
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

	# check if board was already evaluated
	if board.fen() in shared_hash_table:
		return shared_hash_table[board.fen()]

	# recursion base case
	if depth <= 0:
		# evaluate current board
		# value = quiescence_search(board, player, alpha, beta)
		score = player * psqt_pypy.board_value_piece_square(board)
		shared_hash_table[board.fen()] = (score, None)
		return score, None

	# null move prunning
	if null_move and depth >= (main_pypy.R+1) and not board.is_check():
		board.push(chess.Move.null())
		score = -negamax_smp(board, depth -1 - main_pypy.R, -player, False, shared_hash_table, -beta, -beta+1)[0]
		board.pop()
		if score >= beta:
			shared_hash_table[board.fen()] = (beta, None)
			return beta, None
		# board.pop()

	best_move = None

	# initializing best_score
	best_score = float("-inf")
	
	# for move in board.legal_moves:
	for move in move_ordering_pypy.organize_moves(board):
		
		# stop search if this node was already added in our hash table
		if board.fen() in shared_hash_table:
			return shared_hash_table[board.fen()]

		# make the move
		board.push(move)

		# if threefold repetition we do not analyze this position
		if board.can_claim_threefold_repetition():
			board.pop()  
			continue

		score = -negamax_smp(board, depth-1, -player, null_move, shared_hash_table, -beta, -alpha)[0]

		# take move back
		board.pop()

		# beta-cutoff
		if score >= beta:
			shared_hash_table[board.fen()] = (score, move)
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

	# add to hash table before returning
	shared_hash_table[board.fen()] = (best_score, best_move)
	return best_score, best_move


def lazy_smp(board, depth, player, null_move):

	# getting number of processors
	nprocs = mp.cpu_count()

	# start manager so that we can share data between processes
	with mp.Manager() as manager:
		
		# create shared hash table
		shared_hash_table = manager.dict()
		processes = []
		
		# start search for all processors from the root node
		for _ in range(nprocs):
			p = mp.Process(target=negamax_smp, args=(board, depth, player, null_move, shared_hash_table))
			p.start()
			processes.append(p)
		
		# wait for any process to finish
		mp.connection.wait([p.sentinel for p in processes])

		# close all ongoing processes
		for p in processes:
			p.terminate()
		
		# return best move for our original board
		return shared_hash_table[board.fen()][1].uci()