from src.main_classes.package import Package


class Column(object):

    """Class represents a column in cargo space.
        Attributes:
            packages: An array, indicating packages for selected column.
            package_count: An integer, indication number of packages in column.
            weight: An integer, indicating sum weight of column.
    """

    def __init__(self, cs_height: int):
        self.packages = [None for i in range(cs_height)]
        self.package_count = 0
        self.weight = 0

    def get_size(self) -> int:
        """Returns size of column.
        :return An integer, indicating maximum number of packages in column.
        """
        return len(self.packages)

    def push(self, package: Package):
        """Adds package into column.
        :param package: An object of type Package, indicating package that will be added in column after last package.
        :return /
        """
        self.packages[self.package_count] = package
        self.package_count += 1
        self.weight += package.weight

    def pop(self) -> object:
        """Returns the most upper package in column.
        :return Package
        """
        self.package_count -= 1
        self.weight -= self.packages[self.package_count].weight
        return self.packages[self.package_count]

    def unload_at_station(self, station_index: int) -> tuple:
        """Unloads packages for specified station.
        :param station_index: An integer, indicating index of station on which simulation is currently at.
        :return A tuple:
                        index 0 -> An array of packages representing waiting que,
                        index 1 -> An integer representing number of movements
        """
        wait_que, mov_sum, wait_que_act = [], 0, False

        for i in range(self.package_count):
            if wait_que_act:
                self.package_count -= 1
                self.weight -= self.packages[i].weight
                wait_que.append(self.packages[i])
                self.packages[i] = None
                mov_sum += 1
                continue
            elif self.packages[i].station_out == station_index:
                self.package_count -= 1
                self.weight -= self.packages[i].weight
                self.packages[i] = None
                wait_que_act = True
                mov_sum += 1

        return wait_que, mov_sum
