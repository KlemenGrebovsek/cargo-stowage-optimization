import os
from functools import partial
from multiprocessing import Pool

from NiaPy.algorithms.basic import *
from NiaPy.algorithms.modified import *
from NiaPy.algorithms.other import *

from src.models.simulation_settings import SimulationSettings
from src.directory.directory import Directory
from src.result_manager.result_manager import ResultManager
from src.runner.runner import Runner


class Simulation:

    def __init__(self, simulation_settings: SimulationSettings):
        """
        :param simulation_settings: SimulationSettings object.
        """
        self._settings = simulation_settings
        self._algorithms = []
        self._save_text = True
        self._save_graph = True
        self._save_gif = True

    def add_algorithm(self, name: str):
        """
        :param name: Algorithm name.
        :return: Bool, indicating whether algorithm is accepted.
        """
        try:
            alg_type = globals()[str(name)]
            alg_obj = alg_type()
            self._algorithms.append(name)

        except NameError as ne:
            print(str(ne))

        except Exception as e:
            print(str(e))

    def remove_algorithm(self, name: str):
        """
        :param name: Algorithm name.
        :return: void
        """
        for i in range(len(self._algorithms)):
            if self._algorithms[i] == name:
                del self._algorithms[i]
                break

    def set_save_options(self, text_file: bool = True, graph: bool = True, gif_animation: bool = True):
        """
        :param text_file: Save results to txt file.
        :param graph: Generate and save results in graph (saved in file).
        :param gif_animation: Generate simulation gif file.
        :return: void
        """
        self._save_text = text_file
        self._save_graph = graph
        self._save_gif = gif_animation

    def simulate(self, n_fes: int = 20, np: int = 30, path: str = '') -> list:
        """
        :param n_fes: Number of total evaluations.
        :param np: Population size.
        :param path: Directory where results will be save in.
        :return: A list, containing optimization results, items -> (algorithm name, fitness, solution, execution time)
        """
        if not os.path.isdir(path):
            print('Simulate: Invalid path.')
            return []

        if n_fes < 1 or np < 1:
            print('Minimum n_fes=1 and minimum np=1.')
            return []

        print('Starting simulation...')
        func = partial(Runner.run, sim_sett=self._settings, n_fes=n_fes, np=np)
        opt_res = Pool().map(func, self._algorithms)
        print('Simulation done.\n')

        if self._save_text or self._save_graph or self._save_gif:
            result_manager = ResultManager(Directory.create(path))

            if self._save_text:
                result_manager.save_txt(opt_res, np, n_fes, self._settings)
            if self._save_graph:
                result_manager.save_graph(opt_res)
            if self._save_gif:
                result_manager.save_gif(self._settings, opt_res)

        return opt_res
