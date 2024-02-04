from enum import Enum

from engines.alpha_beta import AlphaBeta
from engines.l1p_alpha_beta import Layer1ParallelAlphaBeta
from engines.l2p_alpha_beta import Layer2ParallelAlphaBeta
from engines.lazy_smp import LazySMP


class Algorithm(Enum):
    """Enumeration of all possible algorithms."""
    alpha_beta = "alpha_beta"
    parallel_alpha_beta_layer_1 = "parallel_alpha_beta_layer_1"
    parallel_alpha_beta_layer_2 = "parallel_alpha_beta_layer_2"
    lazy_smp = "lazy_smp"


def get_engine(algorithm_name: Algorithm):
    """
    Returns the engine

    Arguments:
        - algorithm_name: the name of the algorithm we want to use.

    Returns:
        - engine: the engine we want to use.
    """
    algorithm_name = Algorithm[algorithm_name]

    if algorithm_name is Algorithm.alpha_beta:
        return AlphaBeta()
    elif algorithm_name is Algorithm.parallel_alpha_beta_layer_1:
        return Layer1ParallelAlphaBeta()
    elif algorithm_name is Algorithm.parallel_alpha_beta_layer_2:
        return Layer2ParallelAlphaBeta()
    elif algorithm_name is Algorithm.lazy_smp:
        return LazySMP()
    raise Exception("algorithm not supported")
