import datetime
import os

from src.model.dataset import Dataset
from src.output_option.output_option import OutputOptionInterface


class TextOutputOption(OutputOptionInterface):

    def __init__(self, **kwargs):
        """
        Args:
            dataset: Used dataset.
            dir_path: Path to dir.
        """

        self._dir_path:     str = kwargs['dir_path']
        self._dataset:      Dataset = kwargs['dataset']
        self._file_name:    str = 'results'

    def save(self, simulation_results: list):
        """Saves simulation results as .txt file.

        Throws ValueError if invalid path or file name.

        Args:
            simulation_results: A list of simulation results.

        Returns: void
        """

        if self._dir_path is None or len(self._dir_path) < 1 or not os.path.isdir(self._dir_path):
            raise ValueError('Invalid dir path')

        if self._file_name is None or len(self._file_name) < 1:
            raise ValueError('Invalid file name')

        full_path = os.path.join(self._dir_path, self._file_name + '.txt')

        if os.path.isfile(full_path):
            raise ValueError('File with that name already exists')

        with open(full_path, 'w') as wr:
            wr.write('----Optimization info---- \n')
            wr.write('Date: %s \n' % datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            wr.write('Algorithms: %s \n \n' % len(simulation_results))
            wr.write('----Dataset info---- \n')
            wr.write('Name : %s \n' % self._dataset.title)
            wr.write('Number of packages : %s \n' % self._dataset.total_packages)
            wr.write('Number of stations : %s \n' % self._dataset.total_stations)
            wr.write('Cargo stowage size : %sx%s \n \n' % (self._dataset.width, self._dataset.height))
            wr.write('----Optimization results---- \n')

            for sim_res in simulation_results:
                wr.write('%s (np=%s, nFes=%s), Fitness: %s, ExecutionTime : %s sec \n' % (
                    sim_res.result.algorithm_title, sim_res.result.np, sim_res.result.n_fes,
                    sim_res.result.best_fitness, sim_res.execution_time))
