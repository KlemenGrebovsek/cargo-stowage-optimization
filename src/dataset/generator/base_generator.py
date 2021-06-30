import random

import numpy as np

from src.dataset.generator.ds_generator import DatasetGeneratorInterface
from src.model.dataset import Dataset
from src.domain.package import Package


class BaseDatasetGenerator(DatasetGeneratorInterface):
    """Base dataset generator.
    """

    def make(self, title: str, pack_c: int, stat_n: int, cargo_dim: int) -> Dataset:
        """Generates new dataset. Throws ValueError if any.

        Args:
            title: Data set name, without file extension.
            pack_c: Total number of packages.
            stat_n: Total number of stations.
            cargo_dim: Cargo stowage space width and height.

        Returns: Generated dataset.
        """

        self._validate(title, pack_c, stat_n, cargo_dim)
        package_collection = []
        in_index_start = 1
        dist_in = [0 for _ in range(stat_n)]
        dist_out = [0 for _ in range(stat_n)]

        for i in range(1, pack_c + 1, 1):
            if in_index_start == stat_n:
                in_index_start = 1

            station_in = in_index_start
            out_next_station = random.randint(0, 100) > 40
            station_out = station_in + 1 if out_next_station else random.randint(station_in + 1, stat_n)

            dist_in[station_in - 1] += 1
            dist_out[station_out - 1] += 1

            package_collection.append(
                Package(
                    id_num=i,
                    station_in=station_in,
                    station_out=station_out,
                    weight=random.randint(1, 99)
                )
            )

            in_index_start += 1

        # perform final check, so indexes won't go out of bounds of columns
        self._final_check(package_collection, stat_n, cargo_dim * cargo_dim)

        return Dataset(
            title=title,
            total_packages=pack_c,
            total_stations=stat_n,
            width=cargo_dim,
            height=cargo_dim,
            packages=package_collection
        )

    @staticmethod
    def _validate(title: str, pack_c: int, stat_n: int, cargo_dim: int):
        """Validates dataset specs and throws ValueError if any of properties is invalid.

         Args:
            title: Data set name, without file extension.
            pack_c: Total number of packages.
            stat_n: Total number of stations.
            cargo_dim: Cargo stowage space width and height.
        """

        if title is None or len(title) < 1:
            raise ValueError('Invalid dataset title')

        if stat_n < 3:
            raise ValueError('Minimum number of stations is 3.')

        if cargo_dim < 3:
            raise ValueError('Minimum cargo stowage size is 3.')

        if pack_c < 9:
            raise ValueError('Minimum number of packages is 9.')

        third_of_cargo_sp_size = int((cargo_dim * cargo_dim) / 4) * 3

        if third_of_cargo_sp_size < (pack_c / (stat_n - 2)):
            raise ValueError('Maximum allowed number of packages for this size of cargo space and number of'
                             ' stations is {0}'.format(third_of_cargo_sp_size * (stat_n - 2)))

    @staticmethod
    def _final_check(packages: list, stat_n: int, cargo_sp_size: int):
        """Performs final check on generated packages.

        Args:
            packages: List of generated packages.
            stat_n; Total number of stations.
        """

        packages_by_stat_in = [[] for _ in range(stat_n)]
        dist_by_station = [0 for _ in range(stat_n)]
        fake_cargo_space, redo_check, station_num = [], False, 1

        for package in packages:
            packages_by_stat_in[package.station_in - 1].append(package)

        while station_num < stat_n + 1:
            # remove for current station
            remove_counter, remove_size = 0, len(fake_cargo_space)
            while remove_counter < remove_size:
                if fake_cargo_space[remove_counter].station_out == station_num:
                    fake_cargo_space.pop(remove_counter)
                    remove_size -= 1
                else:
                    remove_counter += 1

            # load for station
            for package in packages_by_stat_in[station_num - 1]:
                # add new
                if len(fake_cargo_space) + 1 > cargo_sp_size:
                    min_index = np.argmin(dist_by_station[0:station_num - 1])
                    package.set_station_in(min_index + 1)
                    package.set_station_out(min_index + 2)
                    dist_by_station[min_index] += 1
                    redo_check = True
                else:
                    fake_cargo_space.append(package)

            # save size
            dist_by_station[station_num - 1] += len(fake_cargo_space)

            # redo process if packages where reordered
            if redo_check:
                redo_check, station_num, fake_cargo_space = False, 0, []
                new_packages_by_stat_in = [[] for _ in range(stat_n)]
                dist_by_station = [0 for _ in range(stat_n)]

                for package_station in packages_by_stat_in:
                    for package in package_station:
                        new_packages_by_stat_in[package.station_in - 1].append(package)

                packages_by_stat_in = new_packages_by_stat_in
            station_num += 1
