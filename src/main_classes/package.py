class Package(object):

    """Class represents a package.
    Attributes:
        id: An integer, indicating package identification number.
        station_out: An Integer, indicating index of station at which the package will be unloaded.
        weight: An integer, indicating weight of a package.
        given_col_index: An integer, indicating column of cargo space where package will be loaded.
    """

    def __init__(self, id_num: int, station_out: int, weight: int):
        self.id = id_num
        self.station_out = station_out
        self.weight = weight
        self.given_col_index = 0
