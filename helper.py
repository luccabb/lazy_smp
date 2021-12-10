from enum import Enum
import parallel_alpha_beta
import lazy_smp

class Algorithm(Enum):
    alpha_beta = "alpha_beta"
    parallel_alpha_beta_layer_1 = "parallel_alpha_beta_layer_1"
    parallel_alpha_beta_layer_2 = "parallel_alpha_beta_layer_2"
    lazy_smp = "lazy_smp"

def get_implementation(algorithm_name: Algorithm):
    algorithm_name = Algorithm[algorithm_name]

    if algorithm_name is Algorithm.alpha_beta:
        return parallel_alpha_beta.alpha_beta
    elif algorithm_name is Algorithm.parallel_alpha_beta_layer_1:
        return parallel_alpha_beta.parallel_alpha_beta_layer_1
    elif algorithm_name is Algorithm.parallel_alpha_beta_layer_2:
        return parallel_alpha_beta.parallel_alpha_beta_layer_2
    elif algorithm_name is Algorithm.lazy_smp:
        return lazy_smp.lazy_smp
    raise Exception("algorithm not supported")
    