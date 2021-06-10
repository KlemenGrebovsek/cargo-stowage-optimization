from src.model.simulation_result import SimulationResult


class SimulationRunInfo:
    """ Holds all data from simulation run.
    """

    def __init__(self, completed: bool, has_error: bool, error_msg: str, execution_time: float,
                 result: SimulationResult):
        """
        Args:
            completed: Indicates whether optimization ran to completion without any error.
            has_error: Indicates whether error occurred.
            error_msg: Error msg if error occurred.
            execution_time: Total execution time of optimization in ms.
            result: Result of optimization.
        """

        self._completed:        bool = completed
        self._has_error:        bool = has_error
        self._error_msg:        str = error_msg
        self._execution_time:   float = execution_time
        self._result:           SimulationResult = result

    @property
    def is_completed(self) -> bool:
        return self._completed

    @property
    def has_error(self) -> bool:
        return self._has_error

    @property
    def error_msg(self) -> str:
        return self._error_msg

    @property
    def execution_time(self) -> float:
        return self._execution_time

    @property
    def result(self) -> SimulationResult:
        return self._result
