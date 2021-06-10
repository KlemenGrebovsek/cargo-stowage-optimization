import math
import numpy as np

from src.model.dataset import Dataset
from src.domain.cargo_space import CargoSpace


class BenchmarkC(object):

    def __init__(self, dataset: Dataset):
        self.Lower:                     int = 0
        self.Upper:                     int = 1
        self._dataset:                  Dataset = dataset
        self._packages_by_station:      list = [[] for _ in range(dataset.total_stations)]

        for package in self._dataset.packages:
            self._packages_by_station[package.station_in - 1].append(package)

    def function(self):
        def evaluate(d: int, sol: list) -> int:
            package_movements, sol_index, total_lay_ds, total_we_ds = 0, 0, 0, 0
            cargo_space = CargoSpace(width=self._dataset.width, height=self._dataset.height)

            # Set column boundaries.
            cargo_sp_col_sep = np.linspace(self.Lower, self.Upper, self._dataset.width + 1)
            cargo_sp_col_sep[self._dataset.width] += 0.1

            # Define package column positions via given solution.
            for package in self._dataset.packages:
                package.given_col_index = np.digitize(sol[sol_index], cargo_sp_col_sep) - 1
                sol_index += 1

            # Simulate ship route.
            for station in range(1, self._dataset.total_stations + 1, 1):
                package_movements, layout_col_dev, weight_col_dev \
                    = cargo_space.simulate_stop_at_station(station, self._packages_by_station[station - 1])

                package_movements += package_movements

                # Calculate layout and weight distribution in cargo space.
                for x in range(self._dataset.width):
                    total_lay_ds += abs(layout_col_dev[x] - (sum(layout_col_dev) / len(layout_col_dev)))
                    total_we_ds += abs(weight_col_dev[x] - (sum(weight_col_dev) / len(weight_col_dev)))

            # Return calculated fitness.
            # Probably should find better formula to calculate fitness.
            return int(math.sqrt(package_movements * ((total_lay_ds * 4) * total_we_ds))) * 2
        return evaluate
