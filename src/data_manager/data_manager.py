import os
import random
import csv
from src.models.package import Package
from src.models.simulation_settings import SimulationSettings


class DataManager:

    def __init__(self, path: str):
        """
        :param path: Indicates, path to data set folder.
        """
        self._path = path

    def new(self, ds_name: str, pack_c: int, stat_n: int, cargo_s: int) -> tuple:
        """
        :param ds_name: Data set name, without file extension.
        :param pack_c: Total number of packages.
        :param stat_n: Total number of stations.
        :param cargo_s: Cargo stowage width and height.
        :return: A tuple, (data set generated: bool, error msg: str)
        """

        if not os.path.isdir(self._path):
            return False, 'DataManager: Invalid folder path'

        if stat_n < 5:
            return False, 'Minimum number of stations is 5.'

        if cargo_s < 3:
            return False, 'Minimum cargo stowage size is 3.'

        if pack_c < 9:
            return False, 'Minimum number of packages is 9.'

        try:
            with open("%s/%s.csv" % (self._path, ds_name), 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([pack_c, stat_n, cargo_s, cargo_s])

                for packageCounter in range(1, int(pack_c) + 1, 1):
                    st_out = random.randint(2, int(stat_n))
                    writer.writerow([packageCounter, random.randint(1, st_out - 1), st_out, random.randint(1, 99)])

        except IOError as ioe:
            return False, 'IOError: ' + str(ioe)

        except Exception as e:
            return False, 'Exception: ' + str(e)

        return True, ''

    def read(self, ds_name: str) -> tuple:
        """
        :param ds_name: Data set name, without file extension.
        :return: A tuple, (object: SimulationSettings, error: str)
        """
        if not os.path.isdir(self._path):
            return SimulationSettings(0, [], 0, 0, 0, ''), 'DataManager: Invalid folder path'

        try:
            with open("%s/%s" % (self._path, ds_name), mode='r') as f:
                reader = csv.reader(f, delimiter=',')
                header = next(reader)
                pack_c, stat_n, car_pac_wi, car_spa_he = int(header[0]), int(header[1]), int(header[2]), int(header[3])
                packages = [[] for x in range(stat_n)]

                for row in reader:
                    packages[int(row[1]) - 1].append(Package(int(row[0]), int(row[2]), int(row[3])))

            if pack_c != sum(len(i) for i in packages):
                return SimulationSettings(0, [], 0, 0, 0, ''), 'Data set is invalid.'

        except IOError as ioe:
            return SimulationSettings(0, [], 0, 0, 0, ''), 'IOError: ' + str(ioe)

        except Exception as ex:
            return SimulationSettings(0, [], 0, 0, 0, ''), 'Exception: ' + str(ex)

        return SimulationSettings(pack_c, packages, stat_n, car_pac_wi, car_pac_wi, ds_name), ''
