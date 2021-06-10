import enum
from NiaPy.util import Task, OptimizationType
from NiaPy.algorithms.basic import *
from NiaPy.algorithms.modified import *
from NiaPy.algorithms.other import *

from src.core.runner.runner import Runner
from src.model.dataset import Dataset
from src.save_option.save_option import SaveOptionInterface
from src.core.benchmark.benchmark import BenchmarkC
from multiprocessing.pool import ThreadPool as Pool

import random


class SortAttribute(enum.Enum):
    FITNESS = 0
    EXECUTION_TIME = 1


class Simulation:
    """
    This class is responsible to run genetic algorithm simulation. It's limited to n_fes and np parameters.
    """

    def __init__(self, dataset: Dataset):
        """
        Args:
            dataset: Dataset for simulation.
        """

        self._dataset: Dataset = dataset
        self._algorithms: list = []
        self._save_options: list = []

    def add_algorithm(self, name: str, n_fes: int = 20, np: int = 30):
        """Adds new genetic algorithm to simulation.
        Throws KeyError if algorithm doesn't exists and ValueError n_fes/np value is invalid.

        Args:
            name: A string representing algorithm name.
            n_fes: Total number of evaluations. Default value is 20.
            np: Population size. Default value is 30.

        Returns: Void
        """

        if n_fes < 1 or np < 1:
            raise ValueError('Minimum valid n_fes and np value is 1.')

        if name is None or len(name) < 1:
            raise ValueError('Invalid algorithm name.')

        alg_type = globals()[str(name)]
        alg_obj = alg_type(seed=random.randint(1, 9999), task=Task(D=self._dataset.total_packages,
                                                                   nFES=n_fes,
                                                                   benchmark=BenchmarkC(dataset=self._dataset),
                                                                   optType=OptimizationType.MINIMIZATION), NP=np)
        self._algorithms.append(alg_obj)

    def remove_algorithm(self, name: str) -> bool:
        """Removes first genetic algorithm with that name.
        Throws Exception if algorithm name value is invalid.

        Args:
            name: A string representing algorithm name.

        Returns: A boolean representing, action result.
        """

        if name is None or len(name) < 1:
            raise Exception('Invalid algorithm name.')

        for i in range(len(self._algorithms)):
            if type(self._algorithms[i]).__name__ == name:
                del self._algorithms[i]
                return True

        return False

    def algorithms(self) -> list:
        """Gets all simulation algorithm names.

        Returns: A list of simulation algorithm names.
        """

        return [type(i).__name__ for i in self._algorithms]

    def add_save_option(self, option: SaveOptionInterface):
        """ Adds new simulation result save option.

        Args:
            option: SaveOptionInterface type of object.

        Returns: Void
        """
        self._save_options.append(option)

    def run(self, sort_by_best: SortAttribute):
        """Starts simulation, saves results with save options and returns results.
        Throws Exception if params are not set.

        Args:
            sort_by_best: Sort results by this attribute from the best to the worst one.

        Returns: void

        """

        if len(self._algorithms) < 1 or len(self._save_options) < 1:
            raise Exception('Empty algorithm or save options list')

        pool = Pool()
        opt_res = pool.map(Runner.run, self._algorithms)
        pool.close()
        pool.join()

        if sort_by_best == SortAttribute.FITNESS:
            sorted_res = sorted(opt_res, key=lambda item: item.result.best_fitness)
        else:
            sorted_res = sorted(opt_res, key=lambda item: item.execution_time)

        # trigger all save options sync
        for option in self._save_options:
            option.save(sorted_res)
