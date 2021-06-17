import json

from src.core.simulation.simulation import Simulation, SortAttribute
from src.dataset.reader.csv_reader import CSVDatasetReader
from src.model.output_opt_config import OutputOptionConfig

configFile = '../config/config.json'

if __name__ == '__main__':
    try:
        config_data = json.load(open(configFile, 'r'))
        dataset = CSVDatasetReader().read(config_data['dataset'])

        simulation = Simulation(
            dataset=dataset,
            n_fes=config_data['n_fes'],
            np=config_data['np'],
            save_to_dir=config_data['saveToDir']
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
