from psqt import board_evaluation
import chess


def quiescence_search(board: chess.Board, alpha: float, beta: float) -> float:
    stand_pat = board_evaluation(board)
    
    if(stand_pat >= beta):
        return beta
    if(alpha < stand_pat):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)        
            score = -quiescence_search(board, -beta, -alpha)
            board.pop()

            if(score >= beta):
                return beta
            if(score > alpha):
                alpha = score  
    
    return alpha