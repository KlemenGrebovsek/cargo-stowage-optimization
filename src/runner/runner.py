import timeit
from src.benchmark.benchmark import BenchmarkC
from src.models.simulation_settings import SimulationSettings
from NiaPy.algorithms.basic import *
from NiaPy.algorithms.modified import *
from NiaPy.algorithms.other import *
from NiaPy.util import Task, OptimizationType
import random


class Runner(object):

    @staticmethod
    def run(alg_t: str, sim_sett: SimulationSettings, n_fes: int, np: int) -> tuple:
        """ Starts optimization with the selected algorithm and returns the result.
            :param alg_t: A string, indicating algorithm name
            :param sim_sett: An object, indicating optimization settings.
            :param n_fes: An integer, indicating number of evaluations.
            :param np: An integer, indicating number of population.
            :return A tuple, containing optimization results with given algorithm ( algorithm name, fitness,
             execution time)
        """
        try:
            alg_type = globals()[str(alg_t)]
            alg_obj = alg_type(seed=random.randint(1, 9999), task=Task(D=sim_sett.pack_count, nFES=n_fes,
                                                                       benchmark=BenchmarkC(sim_sett),
                                                                       optType=OptimizationType.MINIMIZATION), NP=np)
            start_t = timeit.default_timer()
            solution, best_fit = alg_obj.run()
            exe_time = round(timeit.default_timer() - start_t, 5)

            return alg_t, best_fit, solution, exe_time

        except NameError as err:
            print(str(err))
            import sys
            return alg_t, sys.maxsize, [], 0

        except Exception as ex:
            print('Unknown exception : %s' % str(ex))
            import sys
            return alg_t, sys.maxsize, [], 0
