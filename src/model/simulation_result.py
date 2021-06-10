class SimulationResult:
    """Holds data for best simulation result.
    """

    def __init__(self, algorithm_title: str, best_fitness: int, best_solution: list, np: int, n_fes: int):
        """
        Args:
            algorithm_title:    Genetic algorithm title.
            best_fitness:       Best calculated fitness.
            best_solution:      Best solution.
            np:                 Population.
            n_fes:              Number of evaluations.
        """

        self._algorithm_title:  str = algorithm_title
        self._best_fitness:     int = best_fitness
        self._best_solution:    list = best_solution
        self._np:               int = np
        self._n_fes:            int = n_fes

    @property
    def algorithm_title(self) -> str:
        return self._algorithm_title

    @property
    def best_fitness(self) -> int:
        return self._best_fitness

    @property
    def best_solution(self) -> list:
        return self._best_solution

    @property
    def np(self) -> int:
        return self._np

    @property
    def n_fes(self) -> int:
        return self._n_fes
