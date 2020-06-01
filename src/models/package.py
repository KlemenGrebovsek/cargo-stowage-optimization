class Package(object):

    def __init__(self, id_num: int, station_out: int, weight: int):
        self.id = id_num
        self.station_out = station_out
        self.weight = weight
        self.given_col_index = 0
