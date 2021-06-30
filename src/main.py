import datetime
import json
import os

from src.core.simulation.simulation import Simulation, SortAttribute
from src.dataset.generator.base_generator import BaseDatasetGenerator
from src.dataset.reader.csv_reader import CSVDatasetReader
from src.dataset.writer.csv_writer import CSVDatasetWriter
from src.model.output_opt_config import OutputOptionConfig

configFile = '../config/config.json'


# use this method to generate new dataset
def generate_data_set():
    try:
        generator = BaseDatasetGenerator()
        csv_writer = CSVDatasetWriter()
        new_ds = generator.make(title='testSet3', pack_c=225, stat_n=5, cargo_dim=10)
        csv_writer.write(dir_path='../datasets', file_name='testSet3', dataset=new_ds)
    except Exception as error:
        print(str(error))


if __name__ == '__main__':
    # generate_data_set()
    try:
        config_data = json.load(open(configFile, 'r'))
        dataset = CSVDatasetReader().read(config_data['dataset'])

        result_dir_path = os.path.join(config_data['saveToDir'], datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.mkdir(path=result_dir_path)

        simulation = Simulation(
            dataset=dataset,
            n_fes=config_data['n_fes'],
            np=config_data['np'],
            save_to_dir=result_dir_path
        )

        for algorithm in config_data['algorithms']:
            simulation.add_algorithm(algorithm)

        save_opt_configs = [OutputOptionConfig(class_name=config['class'],
                                               included_kwargs=config['included_kwargs'])
                            for config in config_data['outputOptions']]

        for output_option in save_opt_configs:
            simulation.add_save_option(output_option)

        simulation.run(sort_by_best=SortAttribute[config_data['sortByBest'].lower()])

    except Exception as e:
        print('Execution stopped with error: {0}'.format(str(e)))
