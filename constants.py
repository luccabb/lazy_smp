"""
Definition of search constants

    NULL_MOVE_R: Null move reduction
    CHECKMATE_SCORE: Score for checkmate
    CHECKMATE_THRESHOLD: Threshold to differentiate 
        checkmates from normal moves

"""
NULL_MOVE_R = 2
CHECKMATE_SCORE = 10**8
CHECKMATE_THRESHOLD =  999*(10**4)
QUIESCENCE_SEARCH_DEPTH = 0