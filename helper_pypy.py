import parallel_alpha_beta_pypy
import lazy_smp_pypy


def get_pypy_implementation(algorithm_name):

    if algorithm_name is "alpha_beta":
        return parallel_alpha_beta_pypy.alpha_beta
    elif algorithm_name is "parallel_alpha_beta_layer_1":
        return parallel_alpha_beta_pypy.parallel_alpha_beta_layer_1
    elif algorithm_name is "parallel_alpha_beta_layer_2":
        return parallel_alpha_beta_pypy.parallel_alpha_beta_layer_2
    elif algorithm_name is "lazy_smp":
        return lazy_smp_pypy.lazy_smp
    raise Exception("algorithm not supported")