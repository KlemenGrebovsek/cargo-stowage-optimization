class SimulationSettings(object):

    """Class represents a data set.
    Attributes:
        pack_count: An integer, indicating total number of packages.
        packages_by_station: A list, indicating lists of packages sorted by station of loading.
        station_n: An integer, indicating total number of stations.
        cs_width: An integer, indicating cargo space width.
        cs_height: An integer, indicating cargo space height.
        ds_name: A string, indicating a data set name.
    """

    def __init__(self, pack_c: int, packages: int, station_n: int, cs_width: int, cs_height: int, ds_name: str):
        self.pack_count = pack_c
        self.packages_by_station = packages
        self.station_n = station_n
        self.cs_width = cs_width
        self.cs_height = cs_height
        self.ds_name = ds_name
