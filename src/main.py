from functools import partial
from multiprocessing import Pool
from src.modules.file import File
from src.modules.runner import Runner
from src.modules.directory import Directory
from src.modules.graph import Graph
from src.modules.imageViz import ImageViz


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
    # Props
    ds_name = 'testSet2'
    population_size = 100
    number_of_evaluations = 20000
    save_to_txt = True
    create_visualisation_gif = True
    create_comparison_graph = True
    algorithms = ['ArtificialBeeColonyAlgorithm', 'FlowerPollinationAlgorithm', 'GeneticAlgorithm', 'BatAlgorithm',
                  'GreyWolfOptimizer', 'ParticleSwarmAlgorithm', 'FireflyAlgorithm', 'HybridBatAlgorithm']

    # Read dataset
    sim_sett, err = File.read_data_set(ds_name)
    if err is not None:
        print(err)
        return

    # Run algorithms
    func = partial(Runner.run, sim_sett=sim_sett, n_fes=number_of_evaluations, np=population_size)
    opt_res = Pool().map(func, algorithms)

    # Save results
    if save_to_txt or create_comparison_graph or create_visualisation_gif:
        dir_p = Directory.create()
        if save_to_txt:
            File.save_to_txt(dir_p, opt_res, population_size, number_of_evaluations, sim_sett)
        if create_visualisation_gif:
            ImageViz.viz_best_sol(sim_sett, dir_p, opt_res)
        if create_comparison_graph:
            Graph.save_graph(opt_res, dir_p)
    print('Done!')


if __name__ == '__main__':
    run_optimization()
