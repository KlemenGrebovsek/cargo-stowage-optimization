from src.models.cs_column import Column
import numpy as np


class CargoSpace(object):

    """Class represents a cargo space.
        Attributes:
            columns: An array, indicating columns in cargo space.
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.columns = [Column(height) for i in range(width)]

    def simulate_stop_at_station(self, station_index: int, packages_to_load: list) -> tuple:
        movements_sum = 0
        wait_que = []
        lay_sum_de = np.zeros(len(self.columns), dtype=int)

        # Simulates process of unloading packages for specified station.
        for index, column in enumerate(self.columns):
            ret_que, ret_movements = column.unload_at_station(station_index)
            movements_sum += ret_movements
            wait_que += ret_que
            lay_sum_de[index] = column.package_count

        # Simulates process of loading packages for specified station.
        for package in packages_to_load:
            add_p = np.argmin(lay_sum_de) if lay_sum_de[package.given_col_index] == self.height - 1 \
                else package.given_col_index
            self.columns[add_p].push(package)
            lay_sum_de[add_p] += 1
            movements_sum += 1

        # Loading packages from waiting que.
        for w_package in wait_que:
            add_p = int(np.argmin(lay_sum_de))
            self.columns[add_p].push(w_package)
            lay_sum_de[add_p] += 1
            movements_sum += 1

        return movements_sum, lay_sum_de, [column.weight for column in self.columns]
