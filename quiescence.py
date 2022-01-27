from psqt import board_evaluation
import chess
from move_ordering import organize_moves_quiescence


def quiescence_search(board: chess.Board, alpha: float, beta: float, depth: int) -> float:
    stand_pat = board_evaluation(board)

    if depth == 0 or board.is_checkmate():
        return stand_pat
    
    if(stand_pat >= beta):
        return beta
    if(alpha < stand_pat):
        alpha = stand_pat

    moves = organize_moves_quiescence(board)

    for move in moves:
        board.push(move)        
        score = -quiescence_search(board, -beta, -alpha, depth-1)
        board.pop()

        if(score >= beta):
            return beta
        if(score > alpha):
            alpha = score  
    
    return alpha