import timeit

from src.model.simulation_result import OptimizationResult
from src.model.simulation_run_info import SimulationRunInfo


class Runner:

    @staticmethod
    def run(alg_obj) -> SimulationRunInfo:
        """Starts optimization with the genetic algorithm.

        Args:
            alg_obj: Genetic algorithm object.

        Returns: SimulationRunInfo obj containing info about optimization run.
        """

        try:
            start_t = timeit.default_timer()
            best_solution, best_fitness = alg_obj.run()
            end_t = timeit.default_timer()

            return SimulationRunInfo(
                completed=True,
                has_error=False,
                error_msg='',
                execution_time=round(end_t - start_t, 5),
                result=OptimizationResult(
                    algorithm_title=type(alg_obj).__name__,
                    best_fitness=best_fitness,
                    best_solution=best_solution,
                    np=alg_obj.NP,
                    n_fes=alg_obj.task.nFES
                )
            )

        except Exception as e:
            return SimulationRunInfo(
                completed=False,
                has_error=True,
                error_msg='{0}: {1}'.format(type(alg_obj).__name__, str(e)),
                execution_time=-1,
                result=OptimizationResult(
                    algorithm_title='',
                    best_fitness=0,
                    best_solution=[],
                    np=0,
                    n_fes=0
                )
            )
