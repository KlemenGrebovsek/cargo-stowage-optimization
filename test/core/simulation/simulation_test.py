import unittest

from src.model.dataset import Dataset
from src.core.simulation.simulation import Simulation


class SimulationTest(unittest.TestCase):
    def test_simulation_add_algorithm_empty(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset)
            simulation.add_algorithm('')
            self.fail('Invalid algorithm name was accepted')
        except ValueError:
            pass

    def test_simulation_add_algorithm_invalid(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset)
            simulation.add_algorithm('invalidName')
            self.fail('Invalid algorithm name was accepted')
        except KeyError:
            pass

    def test_simulation_add_algorithm_invalid_nFes(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset)
            simulation.add_algorithm('GreyWolfOptimizer', n_fes=0)
            self.fail('Invalid nFes was accepted')
        except ValueError:
            pass

    def test_simulation_add_algorithm_invalid_np(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset)
            simulation.add_algorithm('GreyWolfOptimizer', np=0)
            self.fail('Invalid nFes was accepted')
        except ValueError:
            pass

    def test_simulation_add_algorithm_valid_np_nFes(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset)
            simulation.add_algorithm('GreyWolfOptimizer', np=50, n_fes=100)
        except ValueError:
            self.fail('Valid nFes and np was not accepted')

    def test_simulation_add_algorithm_valid(self):
        try:
            dataset = Dataset('name', 30, 5, 5, 5, [])
            simulation = Simulation(dataset=dataset)
            simulation.add_algorithm('GreyWolfOptimizer')
            simulation.add_algorithm('GeneticAlgorithm')
        except ValueError:
            self.fail('Valid algorithm name was not accepted')

    def test_simulation_get_algorithms_values(self):
        dataset = Dataset('name', 30, 5, 5, 5, [])
        simulation = Simulation(dataset=dataset)

        simulation.add_algorithm('GreyWolfOptimizer')
        simulation.add_algorithm('GeneticAlgorithm')
        algorithms = simulation.algorithms()

        self.assertEqual('GreyWolfOptimizer', algorithms[0])
        self.assertEqual('GeneticAlgorithm', algorithms[1])

    def test_simulation_remove_algorithm_valid(self):
        dataset = Dataset('name', 30, 5, 5, 5, [])
        simulation = Simulation(dataset=dataset)

        simulation.add_algorithm('GreyWolfOptimizer')
        simulation.add_algorithm('GeneticAlgorithm')

        if not simulation.remove_algorithm('GreyWolfOptimizer'):
            self.fail('Failed to remove algorithm')

    def test_simulation_remove_algorithm_invalid(self):
        dataset = Dataset('name', 30, 5, 5, 5, [])
        simulation = Simulation(dataset=dataset)

        simulation.add_algorithm('GreyWolfOptimizer')
        simulation.add_algorithm('GeneticAlgorithm')

        if simulation.remove_algorithm('invalidAlgorithm'):
            self.fail('Failed to remove algorithm')

    def test_simulation_remove_algorithm_values(self):
        dataset = Dataset('name', 30, 5, 5, 5, [])
        simulation = Simulation(dataset=dataset)

        simulation.add_algorithm('GreyWolfOptimizer')
        simulation.add_algorithm('GeneticAlgorithm')

        _ = simulation.remove_algorithm('GeneticAlgorithm')

        algorithms = simulation.algorithms()

        self.assertEqual(algorithms[0], 'GreyWolfOptimizer')
        self.assertEqual(1, len(algorithms))
