from src.domain.package import Package


class Column:

    """Represents column in cargo stowage place.
    """

    def __init__(self, height: int):
        """
        Args:
            height: Column height.
        """

        self._values:           list = [None for _ in range(height)]
        self._package_count:    int = 0
        self._sum_weight:       int = 0

    @property
    def sum_weight(self) -> int:
        return self._sum_weight

    def get_height(self) -> int:
        """Gets column size.

        Returns: Column size.
        """

        return len(self._values)

    def count(self) -> int:
        """ Returns total packages in column.

        Returns: Package count.
        """

        return self._package_count

    def add(self, package: Package):
        """Adds new package on top of column.

        Args:
            package: Package to add.

        Returns: void
        """

        self._values[self._package_count] = package
        self._package_count += 1
        self._sum_weight += package.weight

    def get(self, index: int) -> Package:
        """ Returns value at index.

        Args:
            index: Index of value.

        Returns: Value at index.
        """
        return self._values[index]

    def pop(self) -> Package:
        """ Removes and returns the package with max index in column.
        If empty returns None.

        Returns: Package or None.
        """

        self._package_count -= 1
        self._sum_weight -= 0 if self._values[self._package_count] is None \
            else self._values[self._package_count].weight

        return self._values[self._package_count]

    def unload_at_station(self, station_index: int) -> tuple:
        """ Unloads packages at given station, counts movements, and creates waiting que of packages to be loaded back
        if needed.

        Args:
            station_index: Current station index (out).

        Returns: list of temp queue packets, sum of package movements
        """

        wait_que, mov_sum, wait_que_act = [], 0, False

        for i in range(self._package_count):
            if wait_que_act:
                wait_que.append(self._values[i])
            elif self._values[i].station_out == station_index:
                wait_que_act = True
            self._package_count -= 1
            self._sum_weight -= 0 if self._values[i] is None else self._values[i].weight
            self._values[i] = None
            mov_sum += 1

        return wait_que, mov_sum
