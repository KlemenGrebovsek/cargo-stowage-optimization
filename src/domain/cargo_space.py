from numpy import ndarray

from src.domain.cs_column import Column
import numpy as np

from src.model.stop_at_station_summary import StopAtStationSummary


class CargoSpace(object):
    """ Represents cargo space in transport vehicle/ship ect.
    """

    def __init__(self, width: int, height: int):
        self._width:    int = width
        self._height:   int = height
        self._columns:  list = [Column(height) for i in range(width)]

    @property
    def columns(self) -> list:
        return self._columns

    def simulate_stop_at_station(self, station_index: int, packages_to_load: list) -> StopAtStationSummary:
        """ Simulates stop at station, unloads, loads packages and monitors activities.

        Args:
            station_index: Current station index.
            packages_to_load: List of packages to load at this station.

        Returns: Summary of process and current state of cargo space.
        """

        movements_sum = 0
        wait_que = []
        packages_per_col = np.zeros(len(self._columns), dtype=int)

        # Unload packages for current station.
        movements_sum += self._unload_packages(packages_per_col, wait_que, station_index)

        # Load packages for current station.
        movements_sum += self._load_packages(packages_to_load, packages_per_col)

        # Load packages from waiting que.
        movements_sum += self._load_packages(wait_que, packages_per_col)

        return StopAtStationSummary(
            movements_sum=movements_sum,
            layout_dist=packages_per_col.tolist(),
            weight_dist=[column.sum_weight for column in self._columns]
        )

    def _unload_packages(self, packages_per_col: ndarray, wait_que: list, station_index: int) -> int:
        movement = 0
        for index, column in enumerate(self._columns):
            ret_que, ret_movements = column.unload_at_station(station_index)
            movement += ret_movements
            wait_que += ret_que
            packages_per_col[index] = column.count()

        return movement

    def _load_packages(self, packages_to_load: list, packages_per_col: ndarray) -> int:
        movements = 0
        for package in packages_to_load:
            add_index = package.given_col_index

            if packages_per_col[add_index] == self._height:
                add_index = np.argmin(packages_per_col)

            self._columns[add_index].add(package)
            packages_per_col[add_index] += 1
            movements += 1

        return movements
