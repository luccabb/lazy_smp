from enum import Enum

from engines.alpha_beta import AlphaBeta
from engines.l1p_alpha_beta import Layer1ParallelAlphaBeta
from engines.l2p_alpha_beta import Layer2ParallelAlphaBeta
from engines.lazy_smp import LazySMP
from engines.random import RandomEngine
from config import Config


class Algorithm(Enum):
    """Enumeration of all possible algorithms."""

    alpha_beta = "alpha_beta"
    parallel_alpha_beta_layer_1 = "parallel_alpha_beta_layer_1"
    parallel_alpha_beta_layer_2 = "parallel_alpha_beta_layer_2"
    lazy_smp = "lazy_smp"
    random = "random"


def get_engine(config: Config):
    """
    Returns the engine

    Arguments:
        - algorithm_name: the name of the algorithm we want to use.

    Returns:
        - engine: the engine we want to use.
    """
    algorithm = Algorithm[config.algorithm]

    if algorithm is Algorithm.alpha_beta:
        return AlphaBeta(config)
    elif algorithm is Algorithm.parallel_alpha_beta_layer_1:
        return Layer1ParallelAlphaBeta(config)
    elif algorithm is Algorithm.parallel_alpha_beta_layer_2:
        return Layer2ParallelAlphaBeta(config)
    elif algorithm is Algorithm.lazy_smp:
        return LazySMP(config)
    elif algorithm is Algorithm.random:
        return RandomEngine(config)
    raise Exception("algorithm not supported")
