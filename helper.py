from enum import Enum
from parallel_alpha_beta import alpha_beta, parallel_alpha_beta_layer_1, parallel_alpha_beta_layer_2
from lazy_smp import LazySMP
from alpha_beta import AlphaBeta
from l1p_alpha_beta import Layer1ParallelAlphaBeta

# Search constants
NULL_MOVE_R = 2
CHECKMATE_SCORE = 10**8
CHECKMATE_THRESHOLD =  999*(10**6)

class Algorithm(Enum):
    alpha_beta = "alpha_beta"
    parallel_alpha_beta_layer_1 = "parallel_alpha_beta_layer_1"
    parallel_alpha_beta_layer_2 = "parallel_alpha_beta_layer_2"
    lazy_smp = "lazy_smp"

def get_engine(algorithm_name: Algorithm):
    algorithm_name = Algorithm[algorithm_name]

    if algorithm_name is Algorithm.alpha_beta:
        return AlphaBeta()
    elif algorithm_name is Algorithm.parallel_alpha_beta_layer_1:
        return Layer1ParallelAlphaBeta()
    elif algorithm_name is Algorithm.parallel_alpha_beta_layer_2:
        return parallel_alpha_beta_layer_2
    elif algorithm_name is Algorithm.lazy_smp:
        return LazySMP()
    raise Exception("algorithm not supported")
    