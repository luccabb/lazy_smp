"""
Definition of search constants

    ALGORITHM_NAME: Algorithm to use to search move.
        - alphabeta: alphabeta search.
        - parallel_alpha_beta_layer_1: parallel alpha beta search from 1st ply.
        - parallel_alpha_beta_layer_2: parallel alpha beta search from 2nd ply.
        - lazy_smp: lazy smp search.
    DEPTH: Depth of search.
    NULL_MOVE: If True, use null move prunning.
    NULL_MOVE_R: Null move reduction factor.
    CHECKMATE_SCORE: Score for checkmate.
    CHECKMATE_THRESHOLD: Threshold to differentiate 
        checkmates from other moves.
    QUIESCENCE_SEARCH_DEPTH: Depth to search in quiescence search.

"""
ALGORITHM_NAME = "parallel_alpha_beta_layer_2"
NEGAMAX_DEPTH = 5
NULL_MOVE = True
NULL_MOVE_R = 2
CHECKMATE_SCORE = 10**8
CHECKMATE_THRESHOLD =  999*(10**4)
QUIESCENCE_SEARCH_DEPTH = 3
