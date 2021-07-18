import os
from datetime import datetime

from NiaPy.util import Task, OptimizationType

# NiaPy algorithms
from NiaPy.algorithms.basic import *
from NiaPy.algorithms.modified import *
from NiaPy.algorithms.other import *

# Output options
from src.model.output_opt_config import OutputOptionConfig
from src.output_option.output_option import OutputOptionInterface
from src.output_option.console_output import ConsoleOutputOption
from src.output_option.txt_output import TextOutputOption
from src.output_option.graph_output import GraphOutputOption
from src.output_option.gif_output import GifOutputOption

from src.core.runner.runner import Runner
from src.core.simulation.simulation_errors import InvalidAlgorithmName, InvalidSaveOptionName, \
    InvalidSimulationInitialState
from src.logger.logger import Logger
from src.model.dataset import Dataset
from src.model.sort_attribute import SortAttribute
from src.core.benchmark.benchmark import BenchmarkC
from multiprocessing.pool import ThreadPool as Pool

import random


class Simulation:
    """
    This class is responsible to run genetic algorithms simulation. It's limited to n_fes and np parameters.
    """

    def __init__(self, dataset: Dataset, n_fes: int, np: int, save_to_dir: str):
        """
        Args:
            dataset: Dataset of simulation.
            n_fes Total number of evaluations.
            np: Population size.
            save_to_dir: Path to directory where simulation results will be stored.
        """

        random.seed(n_fes + np + datetime.now().second)
        self.logger = Logger(self.__class__.__name__)

        self.n_fes = n_fes
        self.logger.console_log('n_fes value set to {0}'.format(n_fes))

        self.np = np
        self.logger.console_log('np value set to {0}'.format(np))

        self._dataset: Dataset = dataset
        self.logger.console_log('dataset {0}'.format(dataset.title))

        self._algorithms: list = []
        self._save_options: list = []

        self._save_option_kwargs = {
            'dir_path': save_to_dir,
            'dataset': dataset
        }

    def add_algorithm(self, name: str) -> None:
        """Adds new genetic algorithm to simulation.

        Args:
            name: A string representing algorithm name.
        """

        if name is None or len(name) < 1:
            raise InvalidAlgorithmName('Invalid algorithm name "{0}"'.format(name))

        try:
            alg_type = globals()[str(name)]
            alg_obj = alg_type(seed=random.randint(1, 9999), task=Task(D=self._dataset.total_packages,
                                                                       nFES=self.n_fes,
                                                                       benchmark=BenchmarkC(dataset=self._dataset),
                                                                       optType=OptimizationType.MINIMIZATION), NP=self.np)
            self._algorithms.append(alg_obj)
            self.logger.console_log('added algorithm {0}'.format(name))

        except Exception:
            raise InvalidAlgorithmName('Invalid algorithm name "{0}"'.format(name))

    def algorithms(self) -> list:
        """Returns all algorithm names in simulation.
        """

        return [type(i).__name__ for i in self._algorithms]

    def add_save_option(self, config: OutputOptionConfig):
        """ Adds new simulation result save option.

        Args:
            config: SaveOptionConfig object.

        Returns: Void
        """

        if config.class_name is None or len(config.class_name) < 1:
            raise InvalidSaveOptionName('Invalid save option name "{0}"'.format(config.class_name))

        try:
            save_option_type = globals()[str(config.class_name)]

            kwargs_dict = {}

            for kwargs_name in config.included_kwargs:
                param = self._save_option_kwargs[kwargs_name]
                if param is not None:
                    kwargs_dict[kwargs_name] = param

            save_option = save_option_type(**kwargs_dict)
            self._save_options.append(save_option)
            self.logger.console_log('{0} save option added'.format(config.class_name))

        except Exception:
            raise InvalidSaveOptionName('Invalid save option name "{0} or kwargs {1}"'.format(config.class_name,
                                                                                              config.included_kwargs))

    def run(self, sort_by_best: SortAttribute) -> None:
        """Starts simulation.

        Args:
            sort_by_best: Results are ordered by this attribute, from best to worst.

        Returns: void
        """

        self.logger.console_log('Validating state')
        self._validate_initial_state()

        self.logger.console_log("Starting optimization tasks")
        self.logger.console_log("Waiting tasks")

        pool = Pool()
        opt_res = pool.map(Runner.run, self._algorithms)
        pool.close()
        pool.join()

        self.logger.console_log("Tasks finished")

        sorted_res = sorted(opt_res, key=lambda item: item.result.best_fitness if sort_by_best == SortAttribute.fitness
                            else item.execution_time)

        if any(res_info.has_error for res_info in sorted_res):
            self.logger.console_log('Not all simulation tasks were successful')
        else:
            self.logger.console_log('All simulation tasks were successful')

        self.logger.console_log("Starting save options")

        for option in self._save_options:
            option.save(sorted_res)

        self.logger.console_log("Done, stopping execution")

    def _validate_initial_state(self):
        if len(self._algorithms) < 1:
            raise InvalidSimulationInitialState('Cannot start simulation with empty list of algorithms')

        if len(self._save_options) < 1:
            raise InvalidSimulationInitialState('Cannot start simulation with empty list of save options')

        if self.n_fes < 1:
            raise InvalidSimulationInitialState('Cannot start simulation with n_fes prop value less than 1')

        if self.np < 1:
            raise InvalidSimulationInitialState('Cannot start simulation with np prop value less than 1')

        if self._dataset is None or len(self._dataset.packages) != self._dataset.total_packages \
                or self._dataset.total_packages == 0 or len(self._dataset.title) < 1:
            raise InvalidSimulationInitialState('Cannot start simulation with invalid dataset')

        stat_count = self._dataset.total_stations

        for package in self._dataset.packages:
            if package.station_in < 1 or package.station_out > stat_count \
                    or not package.station_in < package.station_out:
                raise InvalidSimulationInitialState('Cannot start simulation with invalid dataset')

        dir_path = self._save_option_kwargs['dir_path']

        if dir_path is None or len(dir_path) < 1 or not os.path.isdir(dir_path):
            raise InvalidSimulationInitialState('Cannot start simulation with invalid results dir path')
