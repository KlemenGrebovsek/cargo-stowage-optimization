import math
import numpy as np
from src.models.simulation_settings import SimulationSettings
from src.models.cargo_space import CargoSpace


class BenchmarkC(object):

    def __init__(self, sim_sett: SimulationSettings):
        """
        :param sim_sett: SimulationSettings object.
        """
        self.Lower = 0
        self.Upper = 1
        self.sim_sett = sim_sett

    def function(self):
        def evaluate(d: int, sol: list) -> int:
            """
            :param d: Dimension of a problem.
            :param sol: Given solution for this generation.
            :return: Calculated fitness score.
            """
            total_p_movements, sol_index, total_lay_ds, total_we_ds = 0, 0, 0, 0
            cargo_space = CargoSpace(width=self.sim_sett.cs_width, height=self.sim_sett.cs_height)

            # Define columns.
            cargo_sp_col_sep = np.linspace(self.Lower, self.Upper, self.sim_sett.cs_width + 1)
            cargo_sp_col_sep[self.sim_sett.cs_width] += 0.1

            # Set package positions.
            for grp in self.sim_sett.packages_by_station:
                for pack in grp:
                    pack.given_col_index = np.digitize(sol[sol_index], cargo_sp_col_sep) - 1
                    sol_index += 1

            # Simulate ship route.
            for station in range(1, self.sim_sett.station_n + 1, 1):
                m, l, w = cargo_space.simulate_stop_at_station(station, self.sim_sett.packages_by_station[station - 1])

                total_p_movements += m

                # Calculation of layout and weight distribution in cargo space.
                for x in range(self.sim_sett.cs_width):
                    total_lay_ds += abs(l[x] - (sum(l) / len(l)))
                    total_we_ds += abs(w[x] - (sum(w) / len(w)))

            # Return calculated fitness.
            return int(math.sqrt(total_p_movements * ((total_lay_ds * 4) * total_we_ds))) * 2
        return evaluate
