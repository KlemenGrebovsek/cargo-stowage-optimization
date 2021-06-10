class Package:
    """Represents package in cargo stowage and it's properties."""

    def __init__(self, id_num: int, station_in: int, station_out: int, weight: int):
        """
        Args:
            id_num:         Identification number.
            station_in:     Number of station for loading.
            station_out:    Number of station for unloading.
            weight:         Gross weight.
        """

        self._id = id_num
        self._station_out = station_out
        self._station_in = station_in
        self._weight = weight
        self.given_col_index = 0

    @property
    def id(self) -> int:
        return self._id

    @property
    def station_out(self) -> int:
        return self._station_out

    @property
    def station_in(self) -> int:
        return self._station_in

    @property
    def weight(self) -> int:
        return self._weight
