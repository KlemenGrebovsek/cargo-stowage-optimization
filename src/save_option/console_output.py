from src.save_option.save_option import SaveOptionInterface


class ConsoleOutputSaveOption(SaveOptionInterface):

    def __init__(self, **kwargs):
        pass

    def save(self, simulation_results: list):
        """ Prints results to console.

        Args:
            simulation_results: A list of simulation results.

        Returns: void
        """

        print('+---------------------------------')

        for run_result in simulation_results:

            print('Title:', run_result.result.algorithm_title, )

            if not run_result.has_error:
                print('Execution time:', run_result.execution_time, 'ms')
                print('Fitness:', run_result.result.best_fitness)
            else:
                print(run_result.error_msg, '\n')

            print('+---------------------------------')
