class Dataset:
    """Holds data for specific dataset and it's readonly.
    """

    def __init__(self, title: str, total_packages: int, total_stations: int,
                 width: int, height: int, packages: list):
        """Initializes dataset with given data.

        Args:
            title:              Dataset title.
            total_packages:     Total number of packages.
            total_stations:     Total number of stations.
            width:              Width of cargo stowage space.
            height:             Height of cargo stowage space.
            packages:           Collection of packages
        """

        self._title:            str = title
        self._total_packages:   int = total_packages
        self._total_stations:   int = total_stations
        self._width:            int = width
        self._height:           int = height
        self._packages:         list = packages

    @property
    def title(self) -> str:
        return self._title

    @property
    def total_packages(self) -> int:
        return self._total_packages

    @property
    def total_stations(self) -> int:
        return self._total_stations

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def packages(self) -> list:
        return self._packages
