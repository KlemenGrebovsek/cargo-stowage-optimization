from src.simulation.simulation import Simulation
from src.data_manager.data_manager import DataManager
import sys

if __name__ == '__main__':
    data_manager = DataManager('VALID PATH')

    # Generate new data set
    # data_manager.new('SetName', 30, 5, 4)

    sim_settings, err = data_manager.read('testSet2')

    if err != '':
        print(err)
        sys.exit()

    simulation = Simulation(sim_settings)

    simulation.add_algorithm('GreyWolfOptimizer')
    simulation.add_algorithm('ParticleSwarmAlgorithm')
    simulation.add_algorithm('FireflyAlgorithm')

    simulation.set_save_options(True, True, True)

    sim_results = simulation.simulate(n_fes=150, np=30, path='VALID PATH')

    for res in sim_results:
        print('\n%s, FITNESS:(%s), TIME:(%s)' % (res[0], res[1], res[3]))
