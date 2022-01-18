from psqt import board_evaluation
import chess


def quiescence_search(board: chess.Board, alpha: float, beta: float, depth: int) -> float:
    stand_pat = board_evaluation(board)

    if depth == 0 or board.is_checkmate():
        return stand_pat
    
    if(stand_pat >= beta):
        return beta
    if(alpha < stand_pat):
        alpha = stand_pat

    moves = board.legal_moves

    for move in moves:
        if board.is_capture(move):
            board.push(move)        
            score = -quiescence_search(board, -beta, -alpha)
            board.pop()

            if(score >= beta):
                return beta
            if(score > alpha):
                alpha = score  
    
    return alpha