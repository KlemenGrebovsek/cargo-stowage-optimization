import unittest

from src.core.simulation.simulation_errors import InvalidAlgorithmName
from src.model.dataset import Dataset
from src.core.simulation.simulation import Simulation


class SimulationTest(unittest.TestCase):

    def test_simulation_get_algorithms(self):
        dataset = Dataset('name', 30, 5, 5, 5, [])
        simulation = Simulation(dataset=dataset, n_fes=30, np=5)

        simulation.add_algorithm('GreyWolfOptimizer')
        simulation.add_algorithm('GeneticAlgorithm')
        algorithms = simulation.algorithms()

        self.assertEqual('GreyWolfOptimizer', algorithms[0])
        self.assertEqual('GeneticAlgorithm', algorithms[1])

    def test_simulation_add_algorithm_empty(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5)
            simulation.add_algorithm('')
            self.fail('Empty algorithm name should not be accepted or ignored')
        except InvalidAlgorithmName:
            pass

    def test_simulation_add_algorithm_invalid(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5)
            simulation.add_algorithm('invalidName')
            self.fail('Invalid algorithm name should not be accepted or ignored')
        except InvalidAlgorithmName:
            pass

    def test_simulation_add_algorithm_none(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset, n_fes=30, np=5)
            simulation.add_algorithm(None)
            self.fail('None value should not be accepted or ignored')
        except InvalidAlgorithmName:
            pass

    def test_simulation_add_algorithm_valid(self):
        dataset = Dataset('name', 30, 5, 5, 5, [])
        simulation = Simulation(dataset=dataset, n_fes=30, np=5)
        simulation.add_algorithm('GreyWolfOptimizer')
        simulation.add_algorithm('GeneticAlgorithm')
        added_algorithms = simulation.algorithms()
        self.assertEqual('GreyWolfOptimizer', added_algorithms[0])
        self.assertEqual('GeneticAlgorithm', added_algorithms[1])
