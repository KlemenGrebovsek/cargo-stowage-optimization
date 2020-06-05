from src.simulation.simulation import Simulation
from src.data_manager.data_manager import DataManager

if __name__ == '__main__':
    data_manager = DataManager('../datasets')

    # Generate new data set
    # data_manager.new(ds_name='SetName', pack_c=30, stat_n=5, cargo_s=4)

    sim_settings, err = data_manager.read('testSet2.csv')

    if err != '':
        print(err)
        input('Press any key to close.')

    simulation = Simulation(sim_settings)

    # Algorithms ->  https://niapy.readthedocs.io/en/stable/api/algorithms.html
    simulation.add_algorithm('GreyWolfOptimizer')
    simulation.add_algorithm('ParticleSwarmAlgorithm')
    simulation.add_algorithm('FireflyAlgorithm')

    # Save opt -> (TXT, GRAPH, GIF)
    simulation.set_save_options(True, True, True)

    sim_results = simulation.simulate(n_fes=10, np=50, path='../results')

    for res in sim_results:
        print('\n%s, FITNESS:(%s), TIME:(%s sec)' % (res[0], res[1], res[3]))

    input('Press any key to close.')
