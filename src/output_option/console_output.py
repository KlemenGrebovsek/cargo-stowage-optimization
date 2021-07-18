from src.output_option.output_option import OutputOptionInterface


class ConsoleOutputOption(OutputOptionInterface):

    def __init__(self, **kwargs):
        pass

    def save(self, simulation_results: list):
        """Prints simulation results to the console.

        Args:
            simulation_results: A list of simulation results.

        Returns: void
        """

        print(' ')
        print('+---------------------------------')

        for run_result in simulation_results:

            print('Title:', run_result.result.algorithm_title, )

            if not run_result.has_error:
                print('Fitness:', run_result.result.best_fitness)
                print('Execution time:', run_result.execution_time, 'ms')
            else:
                print(run_result.error_msg, '\n')

            print('+---------------------------------')
