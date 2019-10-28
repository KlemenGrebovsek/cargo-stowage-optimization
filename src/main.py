from functools import partial
from multiprocessing import Pool
from src.modules.file import File
from src.modules.runner import Runner
from src.modules.directory import Directory
from src.modules.graph import Graph
from src.modules.imageViz import ImageViz


# Set optimization properties.
DATA_SET_NAME = 'testSet'

POPULATION_SIZE = 100
NUMBER_OF_EVALUATIONS = 30000

SAVE_TO_TXT = True
CREATE_VISUALIZATION_GIF = True
CRATE_COMPARISON_GRAPH = True

ALGORITHM_LIST = ['ArtificialBeeColonyAlgorithm', 'FlowerPollinationAlgorithm', 'GeneticAlgorithm', 'BatAlgorithm',
                  'GreyWolfOptimizer', 'ParticleSwarmAlgorithm']


def create_new_dataset(ds_name: str, pack_c: int, stat_n: int, cargo_s_w: int, cargo_s_h: int):
    """Calls a function in module File which generates new data set or returns logical errors if any.
     :param ds_name: A string, indicating data set name.
     :param pack_c: An integer, indicating number of total packages (min = 30).
     :param stat_n: An integer, indicating number of stations (min = 5).
     :param cargo_s_w: An integer, indicating cargo space width (min = 5).
     :param cargo_s_h: An integer, indicating cargo space height (min = 5).
    """

    print(File.generate_new_data_set(ds_name, pack_c, stat_n, cargo_s_w, cargo_s_h))


def run_optimization():
    """Starts optimization and stores results according to the settings you specify.
    """

    sim_sett = File.read_data_set(DATA_SET_NAME)
    if sim_sett.ds_name != ' ':
        print('Starting optimization.')
        func = partial(Runner.run, sim_sett=sim_sett, n_fes=NUMBER_OF_EVALUATIONS, np=POPULATION_SIZE)
        opt_res = Pool().map(func, ALGORITHM_LIST)

        if SAVE_TO_TXT or CRATE_COMPARISON_GRAPH or CREATE_VISUALIZATION_GIF:
            dir_p = Directory.create()
            if SAVE_TO_TXT:
                File.save_to_txt(dir_p, opt_res, POPULATION_SIZE, NUMBER_OF_EVALUATIONS, sim_sett)
            if CREATE_VISUALIZATION_GIF:
                ImageViz.viz_best_sol(sim_sett, dir_p, opt_res)
            if CRATE_COMPARISON_GRAPH:
                Graph.save_graph(opt_res, dir_p)
        print('Done!')


if __name__ == '__main__':
    run_optimization()
