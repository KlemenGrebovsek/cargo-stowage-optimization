import os
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from textwrap import wrap

from src.output_option.output_option import OutputOptionInterface


class GraphOutputOption(OutputOptionInterface):

    def __init__(self, **kwargs):
        """
        Args:
            dir_path: Path to dir.
        """

        self._dir_path:     str = kwargs['dir_path']
        self._file_name:    str = 'results'

    def save(self, simulation_results: list):
        """ Saves results as graph into png file.
        Throws ValueError if invalid path or file name.
        Args:
            simulation_results: A list of simulation results.

        Returns: void
        """

        if self._dir_path is None or len(self._dir_path) < 1 or not os.path.isdir(self._dir_path):
            raise ValueError('Invalid dir path')

        if self._file_name is None or len(self._file_name) < 1:
            raise ValueError('Invalid file name')

        names = [x.result.algorithm_title for x in simulation_results]
        labels = ['\n'.join(wrap(x, 10)) for x in names]
        fitness_scores = [x.result.best_fitness for x in simulation_results]
        exe_time = [x.execution_time for x in simulation_results]

        figure(num=None, figsize=(11, 11), dpi=80, facecolor='w', edgecolor='k')
        plt.subplot(2, 1, 1)
        bars = plt.bar(labels, fitness_scores, color='lightblue', width=0.3)
        plt.ylabel('Value')
        plt.title('Fitness score')
        plt.suptitle('Fitness and execution time comparison', fontsize=16)

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, height, height, ha='center', va='bottom')

        plt.subplot(2, 1, 2)
        bars = plt.bar(labels, exe_time, color='pink', width=0.3)
        plt.ylabel('Seconds')
        plt.title('Execution time')

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, height, "{0:.2f}".format(height), ha='center', va='bottom')

        plt.savefig(os.path.join(self._dir_path, self._file_name + '.png'))
