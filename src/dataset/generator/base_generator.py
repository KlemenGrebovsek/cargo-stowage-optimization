import random

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

        if title is None or len(title) < 1:
            raise ValueError('Invalid dataset title')

        if stat_n < 3:
            raise ValueError('Minimum number of stations is 3.')

        if cargo_dim < 3:
            raise ValueError('Minimum cargo stowage size is 3.')

        if pack_c < 9:
            raise ValueError('Minimum number of packages is 9.')

        # Generate packages
        package_collection = []

        for i in range(1, pack_c + 1, 1):
            station_out = random.randint(2, stat_n)
            package_collection.append(
                Package(
                    id_num=i,
                    station_in=random.randint(1, station_out - 1),
                    station_out=station_out,
                    weight=random.randint(1, 99)
                )
            )

        return Dataset(
            title=title,
            total_packages=pack_c,
            total_stations=stat_n,
            width=cargo_dim,
            height=cargo_dim,
            packages=package_collection
        )
