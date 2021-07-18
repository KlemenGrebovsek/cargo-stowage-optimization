import os

from src.domain.cargo_space import CargoSpace
from src.model.dataset import Dataset
from src.model.simulation_run_info import SimulationRunInfo
from src.output_option.output_option import OutputOptionInterface

from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager as fm
import numpy as np
import imageio


def _calc_we_dist(total_w: int, col_we: int) -> int:
    if total_w == 0 or col_we == 0:
        return 0
    return round((100 * col_we) / total_w)


class GifOutputOption(OutputOptionInterface):

    def __init__(self, **kwargs):
        """
        Args:
            dataset: Used dataset.
            dir_path: Path to dir.
        """

        self._dir_path:     str = kwargs['dir_path']
        self._file_name:    str = ''
        self._dataset:      Dataset = kwargs['dataset']

    def save(self, simulation_results: list):
        """ Save best simulation result as .gif file.
        Throws ValueError if invalid path or file name.

        Args:
            simulation_results: A list of simulation results.

        Returns: void
        """

        if self._dir_path is None or len(self._dir_path) < 1 or not os.path.isdir(self._dir_path):
            raise ValueError('Invalid dir path')

        best_sol = min(simulation_results, key=lambda x: x.result.best_fitness)

        self._file_name = best_sol.result.algorithm_title
        full_path = os.path.join(self._dir_path, self._file_name + '.gif')

        if os.path.isfile(full_path):
            raise ValueError('File already exists')

        img_arr = self._simulate_route(best_sol)
        imageio.mimsave(full_path, img_arr, fps=55, loop=0, duration=4)

    def _simulate_route(self, best_run: SimulationRunInfo) -> list:
        total_p_movements, sol_index, total_lay_ds, total_we_ds = 0, 0, 0, 0
        cargo_space = CargoSpace(width=self._dataset.width, height=self._dataset.height)
        min_p_we, max_p_we = 101, 0
        img_arr, col_we_sum = [], [0 for x in range(self._dataset.width)]

        # Define columns.
        cargo_sp_col_sep = np.linspace(0, 1, self._dataset.width + 1)
        cargo_sp_col_sep[self._dataset.width] += 0.1

        # Sort packages by loading station.
        packages_by_station = [[] for _ in range(self._dataset.total_stations)]

        for package in self._dataset.packages:
            packages_by_station[package.station_in - 1].append(package)

        # Define package column positions via given solution. Get min and max weight.
        for package in self._dataset.packages:
            if package.weight > max_p_we:
                max_p_we = package.weight
            if package.weight < min_p_we:
                min_p_we = package.weight
            package.given_col_index = np.digitize(best_run.result.best_solution[sol_index], cargo_sp_col_sep) - 1
            sol_index += 1

        # Set weight groups.
        we_gr = np.linspace(min_p_we, max_p_we, 5)

        big_font = ImageFont.truetype(fm.findfont(fm.FontProperties(family='DejaVu Sans')), 20)
        small_font = ImageFont.truetype(fm.findfont(fm.FontProperties(family='DejaVu Sans')), 8)

        for station in range(1, self._dataset.total_stations, 1):
            stat_image = Image.new('RGB', ((self._dataset.width * 75) + (5 * self._dataset.width) + 50,
                                           ((self._dataset.height * 35) + 200)), color='white')

            draw_obj = ImageDraw.Draw(stat_image)

            x, y = 10, stat_image.height - 65
            x_line = x + (35 * self._dataset.width) + (5 * self._dataset.width) + 10

            draw_obj.text((x, 15), 'Station number: %s' % station, fill='black', font=big_font)

            draw_obj.text((x, 50), 'Before station', fill='black', font=big_font)

            draw_obj.line(((x_line, y + 35), (x_line, y - (25 * self._dataset.height))), fill=50, width=2)

            self._draw_cs(draw_obj, cargo_space, x, y, small_font, col_we_sum, we_gr)

            dr_x = 30 + (35 * self._dataset.width) + (5 * self._dataset.width)
            dr_y = stat_image.height - 65

            draw_obj.text((dr_x, 50), 'After station', fill='black', font=big_font)

            col_we_sum = cargo_space.simulate_stop_at_station(station, packages_by_station[station - 1]).weight_dist

            self._draw_cs(draw_obj, cargo_space, dr_x, dr_y, small_font, col_we_sum, we_gr)

            img_arr.append(stat_image)

        return img_arr

    def _draw_cs(self, dr_: ImageDraw, cs: CargoSpace, cord_x: int, cord_y: int, font: ImageFont, col_w: list,
                 we_grp: tuple):

        reset_x = cord_x
        cs_sum_we = sum(col_w)

        for f in range(0, self._dataset.width, 1):
            dr_.text((cord_x + 12, cord_y + 43), '%s%%' % _calc_we_dist(cs_sum_we, col_w[f]), fill='black')
            cord_x += 40
        cord_x = reset_x

        for y in range(0, self._dataset.width, 1):
            for x in range(0, self._dataset.height, 1):
                curr_pack = cs.columns[x].get(y)
                if curr_pack is not None:
                    rgb = 240 - (25 * np.digitize(curr_pack.weight, we_grp))
                    dr_.rectangle(((cord_x, cord_y), (cord_x + 35, cord_y + 35)), fill=(rgb, rgb, rgb), outline='black')
                    dr_.text((cord_x + 5, cord_y + 5), 'ID: %s' % curr_pack.id, fill='black', font=font)
                    dr_.text((cord_x + 5, cord_y + 20), 'WE: %s' % curr_pack.weight,
                             fill='black', font=font)
                cord_x += 40
            cord_y -= 40
            cord_x = reset_x
