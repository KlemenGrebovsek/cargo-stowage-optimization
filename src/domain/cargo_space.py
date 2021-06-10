from src.domain.cs_column import Column
import numpy as np


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

    def simulate_stop_at_station(self, station_index: int, packages_to_load: list) -> tuple:
        """ Simulates stop at station, unloads, loads packages and monitors activities and statuses.

        Args:
            station_index: Current station index.
            packages_to_load: List of packages to load at this station.

        Returns: A tuple of (total movements in the process (int), layout number of packets per column (list),
         layout sum weight of packets per column (list)
        """

        movements_sum = 0
        wait_que = []
        packages_per_col = np.zeros(len(self._columns), dtype=int)

        # Simulates process of unloading packages for specified station.

        for index, column in enumerate(self._columns):
            ret_que, ret_movements = column.unload_at_station(station_index)
            movements_sum += ret_movements
            wait_que += ret_que
            packages_per_col[index] = column.count()

        # Simulates process of loading packages for specified station.

        for package in packages_to_load:
            # set add index, if column is full, than we need to pick another one.
            add_index = np.argmin(packages_per_col) if packages_per_col[package.given_col_index] == self._height - 1 \
                else package.given_col_index

            self._columns[add_index].add(package)
            packages_per_col[add_index] += 1
            movements_sum += 1

        # Loading packages from waiting que.

        for w_package in wait_que:
            add_index = int(np.argmin(packages_per_col))
            self._columns[add_index].add(w_package)
            packages_per_col[add_index] += 1
            movements_sum += 1

        return movements_sum, packages_per_col, [column.sum_weight for column in self._columns]
