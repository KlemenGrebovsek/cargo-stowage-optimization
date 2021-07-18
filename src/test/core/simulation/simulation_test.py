import unittest

from src.core.simulation.simulation_errors import InvalidAlgorithmName, InvalidSaveOptionName, \
    InvalidSimulationInitialState
from src.domain.package import Package
from src.model.dataset import Dataset
from src.core.simulation.simulation import Simulation
from src.model.output_opt_config import OutputOptionConfig
from src.model.sort_attribute import SortAttribute


class SimulationTest(unittest.TestCase):

    def test_simulation_get_algorithms(self):
        dataset = Dataset('name', 30, 5, 5, 5, [])
        simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='/notNeeded')

        simulation.add_algorithm('GreyWolfOptimizer')
        simulation.add_algorithm('GeneticAlgorithm')
        algorithms = simulation.algorithms()

        self.assertEqual('GreyWolfOptimizer', algorithms[0])
        self.assertEqual('GeneticAlgorithm', algorithms[1])

    def test_simulation_add_algorithm_empty(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='/notNeeded')
            simulation.add_algorithm('')
            self.fail('Empty algorithm name should not be accepted or ignored')
        except InvalidAlgorithmName:
            pass

    def test_simulation_add_algorithm_invalid(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='/notNeeded')
            simulation.add_algorithm('invalidName')
            self.fail('Invalid algorithm name should not be accepted or ignored')
        except InvalidAlgorithmName:
            pass

    def test_simulation_add_algorithm_none(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='/notNeeded')
            simulation.add_algorithm(None)
            self.fail('None value should not be accepted or ignored')
        except InvalidAlgorithmName:
            pass

    def test_simulation_add_algorithm_valid(self):
        dataset = Dataset('name', 30, 5, 5, 5, [])
        simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='/notNeeded')
        simulation.add_algorithm('GreyWolfOptimizer')
        simulation.add_algorithm('GeneticAlgorithm')
        added_algorithms = simulation.algorithms()
        self.assertEqual('GreyWolfOptimizer', added_algorithms[0])
        self.assertEqual('GeneticAlgorithm', added_algorithms[1])

    def test_simulation_add_save_opt_empty_name_string(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='/notNeeded')
            simulation.add_save_option(OutputOptionConfig(class_name='', included_kwargs=['dir_path', 'dataset']))
            self.fail('Empty save option should raise error')
        except InvalidSaveOptionName:
            pass

    def test_simulation_add_save_opt_none_name_string(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='/notNeeded')
            simulation.add_save_option(OutputOptionConfig(class_name=None, included_kwargs=['dir_path', 'dataset']))
            self.fail('None value save option should raise error')
        except InvalidSaveOptionName:
            pass

    def test_simulation_add_save_opt_invalid_name_string(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='/notNeeded')
            simulation.add_save_option(OutputOptionConfig(class_name='Random', included_kwargs=['dir_path', 'dataset']))
            self.fail('Not existing save option should raise error')
        except InvalidSaveOptionName:
            pass

    def test_simulation_add_save_opt_invalid_kwargs(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='/notNeeded')
            simulation.add_save_option(OutputOptionConfig(class_name='GraphOutputOption', included_kwargs=[]))
            self.fail('Invalid save option kwargs should raise error')
        except InvalidSaveOptionName:
            pass

    def test_simulation_add_save_opt_valid_config_args(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='/notNeeded')
            simulation.add_save_option(OutputOptionConfig(class_name='GraphOutputOption',
                                                          included_kwargs=['dir_path']))

        except InvalidSaveOptionName:
            self.fail('Valid save option kwargs was not accepted.')

    def test_simulation_add_save_opt_valid_config_no_args(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='/notNeeded')
            simulation.add_save_option(OutputOptionConfig(class_name='ConsoleOutputOption', included_kwargs=[]))
        except InvalidSaveOptionName:
            self.fail('Valid save option kwargs was not accepted.')

    def test_simulation_should_not_start_with_no_algorithms(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='../results')
            simulation.add_save_option(OutputOptionConfig(class_name='ConsoleOutputOption', included_kwargs=[]))
            simulation.run(sort_by_best=SortAttribute.fitness)
            self.fail("Simulation started with no algorithms")
        except InvalidSimulationInitialState:
            pass

    def test_simulation_should_not_start_with_no_save_options(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='../results')
            simulation.add_algorithm('GreyWolfOptimizer')
            simulation.run(sort_by_best=SortAttribute.fitness)
            self.fail("Simulation started with no algorithms")
        except InvalidSimulationInitialState:
            pass

    def test_simulation_should_not_start_with_invalid_n_fes(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=0, np=5, save_to_dir='../results')
            simulation.add_algorithm('GreyWolfOptimizer')
            simulation.add_save_option(OutputOptionConfig(class_name='ConsoleOutputOption', included_kwargs=[]))
            simulation.run(sort_by_best=SortAttribute.fitness)
            self.fail("Simulation started with no algorithms")
        except InvalidSimulationInitialState:
            pass

    def test_simulation_should_not_start_with_invalid_np(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=0, save_to_dir='../results')
            simulation.add_algorithm('GreyWolfOptimizer')
            simulation.add_save_option(OutputOptionConfig(class_name='ConsoleOutputOption', included_kwargs=[]))
            simulation.run(sort_by_best=SortAttribute.fitness)
            self.fail("Simulation started with no algorithms")
        except InvalidSimulationInitialState:
            pass

    def test_simulation_should_not_start_with_invalid_dataset_no_packages(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='../results')
            simulation.add_algorithm('GreyWolfOptimizer')
            simulation.add_save_option(OutputOptionConfig(class_name='ConsoleOutputOption', included_kwargs=[]))
            simulation.run(sort_by_best=SortAttribute.fitness)
            self.fail("Simulation started with no algorithms")
        except InvalidSimulationInitialState:
            pass

    def test_simulation_should_not_start_with_invalid_dataset_invalid_package_count(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [Package(id_num=1, station_in=1, station_out=3, weight=30)])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='../results')
            simulation.add_algorithm('GreyWolfOptimizer')
            simulation.add_save_option(OutputOptionConfig(class_name='ConsoleOutputOption', included_kwargs=[]))
            simulation.run(sort_by_best=SortAttribute.fitness)
            self.fail("Simulation started with no algorithms")
        except InvalidSimulationInitialState:
            pass

    def test_simulation_should_not_start_with_invalid_dataset_invalid_package_station_in(self):
        try:
            dataset = Dataset('name', 5, 3, 3, 3,
                              [Package(id_num=1, station_in=1, station_out=2, weight=30),
                               Package(id_num=2, station_in=1, station_out=3, weight=30),
                               Package(id_num=3, station_in=0, station_out=2, weight=30),
                               Package(id_num=4, station_in=1, station_out=3, weight=30),
                               Package(id_num=5, station_in=1, station_out=2, weight=30)
                               ])

            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='../results')
            simulation.add_algorithm('GreyWolfOptimizer')
            simulation.add_save_option(OutputOptionConfig(class_name='ConsoleOutputOption', included_kwargs=[]))
            simulation.run(sort_by_best=SortAttribute.fitness)
            self.fail("Simulation started with no algorithms")
        except InvalidSimulationInitialState:
            pass

    def test_simulation_should_not_start_with_invalid_dataset_invalid_package_station_out(self):
        try:
            dataset = Dataset('name', 5, 3, 3, 3,
                              [Package(id_num=1, station_in=1, station_out=2, weight=30),
                               Package(id_num=2, station_in=1, station_out=3, weight=30),
                               Package(id_num=3, station_in=1, station_out=6, weight=30),
                               Package(id_num=4, station_in=1, station_out=3, weight=30),
                               Package(id_num=5, station_in=1, station_out=2, weight=30)
                               ])

            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='../results')
            simulation.add_algorithm('GreyWolfOptimizer')
            simulation.add_save_option(OutputOptionConfig(class_name='ConsoleOutputOption', included_kwargs=[]))
            simulation.run(sort_by_best=SortAttribute.fitness)
            self.fail("Simulation started with no algorithms")
        except InvalidSimulationInitialState:
            pass

    def test_simulation_should_not_start_with_invalid_dataset_invalid_package_station_out_in(self):
        try:
            dataset = Dataset('name', 5, 3, 3, 3,
                              [Package(id_num=1, station_in=1, station_out=2, weight=30),
                               Package(id_num=2, station_in=1, station_out=3, weight=30),
                               Package(id_num=3, station_in=3, station_out=3, weight=30),
                               Package(id_num=4, station_in=1, station_out=3, weight=30),
                               Package(id_num=5, station_in=1, station_out=2, weight=30)
                               ])

            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='../results')
            simulation.add_algorithm('GreyWolfOptimizer')
            simulation.add_save_option(OutputOptionConfig(class_name='ConsoleOutputOption', included_kwargs=[]))
            simulation.run(sort_by_best=SortAttribute.fitness)
            self.fail("Simulation started with no algorithms")
        except InvalidSimulationInitialState:
            pass

    def test_simulation_should_not_start_with_invalid_dir_path(self):
        try:
            dataset = Dataset('name', 5, 3, 3, 3,
                              [Package(id_num=1, station_in=1, station_out=2, weight=30),
                               Package(id_num=2, station_in=2, station_out=3, weight=30),
                               Package(id_num=3, station_in=1, station_out=3, weight=30),
                               Package(id_num=4, station_in=2, station_out=3, weight=30),
                               Package(id_num=5, station_in=1, station_out=2, weight=30)
                               ])

            simulation = Simulation(dataset=dataset, n_fes=30, np=5, save_to_dir='../invalidDir')
            simulation.add_algorithm('GreyWolfOptimizer')
            simulation.add_save_option(OutputOptionConfig(class_name='ConsoleOutputOption', included_kwargs=[]))
            simulation.run(sort_by_best=SortAttribute.fitness)
            self.fail("Simulation started with no algorithms")
        except InvalidSimulationInitialState:
            pass
