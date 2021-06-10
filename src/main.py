import datetime
import os

from src.core.simulation.simulation import Simulation, SortAttribute
from src.dataset.reader.csv_reader import CSVDatasetReader
from src.save_option.console_output import ConsoleOutputSaveOption
from src.save_option.gif_output import GifOutputSaveOption
from src.save_option.graph_output import GraphOutputSaveOption
from src.save_option.txt_output import TextOutputSaveOption

# Consts
RESULT_DIR = '../results'
DATASET_DIR = '../datasets'
POPULATION_SIZE = 50
N_FES = 20000

# Algorithms ->  https://niapy.readthedocs.io/en/stable/api/algorithms.html

if __name__ == '__main__':
    try:
        dataset = CSVDatasetReader().read(os.path.join(DATASET_DIR, 'testSet2.csv'))
        simulation = Simulation(dataset=dataset)

        simulation.add_algorithm('GeneticAlgorithm', np=POPULATION_SIZE, n_fes=N_FES)
        simulation.add_algorithm('FlowerPollinationAlgorithm', np=POPULATION_SIZE, n_fes=N_FES)
        simulation.add_algorithm('GreyWolfOptimizer', np=POPULATION_SIZE, n_fes=N_FES)
        simulation.add_algorithm('ArtificialBeeColonyAlgorithm', np=POPULATION_SIZE, n_fes=N_FES)
        simulation.add_algorithm('ParticleSwarmAlgorithm', np=POPULATION_SIZE, n_fes=N_FES)
        simulation.add_algorithm('BatAlgorithm', np=POPULATION_SIZE, n_fes=N_FES)

        # create folder to store results
        result_dir_path = os.path.join(RESULT_DIR, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.mkdir(path=result_dir_path)

        simulation.add_save_option(ConsoleOutputSaveOption())
        simulation.add_save_option(GraphOutputSaveOption(dir_path=result_dir_path, file_name='graph123'))
        simulation.add_save_option(TextOutputSaveOption(dataset=dataset, dir_path=result_dir_path, file_name='textFile123'))
        simulation.add_save_option(GifOutputSaveOption(dataset=dataset, dir_path=result_dir_path))

        simulation.run(sort_by_best=SortAttribute.FITNESS)

    except Exception as e:
        print(e)
