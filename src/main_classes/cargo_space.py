from src.main_classes.cs_column import Column
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
        """Simulates full process of loading and unloading at stop station.
        :param station_index: An integer, indicating index of station on which simulation is currently at.
        :param packages_to_load: A list, indicating packages to be loaded at current station.
        :return A tuple :
                        index 0 -> An integer, indicating total number of movements.
                        index 1 -> A list, indicating packages layout distribution in cargo space.
                        index 2 -> A list, indicating weight distribution in cargo space.
        """

        movements_sum, wait_que, lay_sum_de = 0, [], np.zeros(len(self.columns), dtype=int)

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
