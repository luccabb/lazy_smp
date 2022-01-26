from enum import Enum
from parallel_alpha_beta import alpha_beta, parallel_alpha_beta_layer_1, parallel_alpha_beta_layer_2
from lazy_smp import LazySMP

class Algorithm(Enum):
    alpha_beta = "alpha_beta"
    parallel_alpha_beta_layer_1 = "parallel_alpha_beta_layer_1"
    parallel_alpha_beta_layer_2 = "parallel_alpha_beta_layer_2"
    lazy_smp = "lazy_smp"

def get_implementation(algorithm_name: Algorithm):
    algorithm_name = Algorithm[algorithm_name]

    if algorithm_name is Algorithm.alpha_beta:
        return alpha_beta
    elif algorithm_name is Algorithm.parallel_alpha_beta_layer_1:
        return parallel_alpha_beta_layer_1
    elif algorithm_name is Algorithm.parallel_alpha_beta_layer_2:
        return parallel_alpha_beta_layer_2
    elif algorithm_name is Algorithm.lazy_smp:
        return LazySMP()
    raise Exception("algorithm not supported")
    