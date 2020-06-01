import datetime
import os
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from textwrap import wrap
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import imageio

from src.models.package import Package
from src.models.simulation_settings import SimulationSettings
from src.models.cargo_space import CargoSpace


class ResultManager:

    def __init__(self, path: str):
        self._path = path

    def save_txt(self, results: list, np: int, n_fes: int, sim_settings: SimulationSettings):
        if not os.path.isdir(self._path):
            print('save_txt: Invalid path.')
            return

        print('Save_text: %s/simInfo.txt.' % self._path)
        try:
            with open('%s/simInfo.txt' % self._path, 'w') as wr:
                wr.write('----Optimization info---- \n')
                wr.write('Date: %s \n' % datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
                wr.write('Algorithms: %s \n \n' % len(results))
                wr.write('----Dataset info---- \n')
                wr.write('Name : %s \n' % sim_settings.ds_name)
                wr.write('Number of packages : %s \n' % sim_settings.pack_count)
                wr.write('Number of stations : %s \n' % sim_settings.station_n)
                wr.write('Cargo stowage size : %sx%s \n \n' % (sim_settings.cs_width, sim_settings.cs_height))
                wr.write('----EA properties----\n')
                wr.write('Population size : %s \n' % np)
                wr.write('Number of evaluations : %s \n \n' % n_fes)
                wr.write('----Optimization results---- \n')

                for result in results:
                    wr.write('%s, Fitness: %s, ExecutionTime : %s sec \n' % (result[0], result[1], round(result[3], 5)))

        except IOError as ioe:
            print('IO exception : %s.' % str(ioe))

        except Exception as e:
            print('Other exception: %s' % str(e))

    def save_graph(self, results: list):
        if not os.path.isdir(self._path):
            print('save_graph: Invalid path.')
            return

        try:
            print('Save_graph: %s/graph.png' % self._path)
            names = [x[0] for x in results]
            labels = ['\n'.join(wrap(l, 10)) for l in names]
            fitness_scores = [y[1] for y in results]
            exe_time = [i[3] for i in results]

            figure(num=None, figsize=(11, 11), dpi=80, facecolor='w', edgecolor='k')
            plt.subplot(2, 1, 1)
            bars = plt.bar(labels, fitness_scores, color='lightblue', width=0.3)
            plt.ylabel('Value')
            plt.title('Fitness score')
            plt.suptitle('Fitness and execution time comparison', fontsize=16)

            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')
            plt.subplot(2, 1, 2)
            bars = plt.bar(labels, exe_time, color='pink', width=0.3)
            plt.ylabel('Seconds')

            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')
            plt.title('Execution time')
            plt.savefig('%s/graph.png' % self._path)

        except Exception as e:
            print('Save graph: ' + str(e))

    def save_gif(self, sim_sett: SimulationSettings, results: list):
        if not os.path.isdir(self._path):
            print('save_gif: Invalid path.')
            return

        best_sol = min(results, key=lambda x: x[1])
        print('Save_gif: %s/%s.gif' % (self._path, best_sol[0]))
        img_arr = self._simulate_route(sim_sett, best_sol)
        imageio.mimsave('%s/%s.gif' % (self._path, best_sol[0]), img_arr, fps=55, loop=0, duration=4)

    def _simulate_route(self, sim_sett: SimulationSettings, res: list) -> list:
        total_p_movements, sol_index, total_lay_ds, total_we_ds = 0, 0, 0, 0
        cargo_space = CargoSpace(width=sim_sett.cs_width, height=sim_sett.cs_height)
        min_p_we, max_p_we = 101, 0
        img_arr, col_we_sum = [], [0 for x in range(sim_sett.cs_width)]

        # Define columns.
        cargo_sp_col_sep = np.linspace(0, 1, sim_sett.cs_width + 1)
        cargo_sp_col_sep[sim_sett.cs_width] += 0.1

        # Set package positions and get min and max weight of packages. Res[2] = given solution.
        for grp in sim_sett.packages_by_station:
            for pack in grp:
                if pack.weight > max_p_we:
                    max_p_we = pack.weight
                if pack.weight < min_p_we:
                    min_p_we = pack.weight
                pack.given_col_index = np.digitize(res[2][sol_index], cargo_sp_col_sep) - 1
                sol_index += 1

        # Set weight groups.
        we_gr = np.linspace(min_p_we, max_p_we, 5)

        # Drawing cluster.
        for station in range(1, sim_sett.station_n, 1):
            stat_image = Image.new('RGB', ((sim_sett.cs_width * 75) + (5 * sim_sett.cs_width) + 50,
                                           ((sim_sett.cs_height * 35) + 200)), color='white')
            draw_obj = ImageDraw.Draw(stat_image)
            x, y = 10, stat_image.height - 65
            x_line = x + (35 * sim_sett.cs_width) + (5 * sim_sett.cs_width) + 10
            draw_obj.text((x, 15), 'Station number: %s' % station, fill='black',
                          font=ImageFont.truetype('arial.ttf', 20))
            draw_obj.text((x, 50), 'Cargo space before station', fill='black', font=ImageFont.truetype('arial.ttf', 20))
            draw_obj.line(((x_line, y + 35), (x_line, y - (25 * sim_sett.cs_height))), fill=50, width=2)
            self._draw_cs(draw_obj, cargo_space, x, y, ImageFont.truetype('arial.ttf', 8), col_we_sum, we_gr)
            dr_x = 30 + (35 * sim_sett.cs_width) + (5 * sim_sett.cs_width)
            dr_y = stat_image.height - 65
            draw_obj.text((dr_x, 50), 'Cargo space after station', fill='black',
                          font=ImageFont.truetype('arial.ttf', 20))

            m, l, col_we_sum = cargo_space.simulate_stop_at_station(station, sim_sett.packages_by_station[station - 1])

            self._draw_cs(draw_obj, cargo_space, dr_x, dr_y, ImageFont.truetype('arial.ttf', 8), col_we_sum, we_gr)
            img_arr.append(stat_image)
        return img_arr

    def _draw_cs(self, dr_: ImageDraw, cs: CargoSpace, cord_x: int, cord_y: int, font: ImageFont, col_w: list,
                 we_grp: tuple):

        reset_x = cord_x
        cs_sum_we = sum(col_w)

        for f in range(0, len(cs.columns), 1):
            dr_.text((cord_x + 12, cord_y + 43), '%s%%' % self._calc_we_dist(cs_sum_we, col_w[f]), fill='black')
            cord_x += 40
        cord_x = reset_x

        for y in range(0, len(cs.columns), 1):
            for x in range(0, len(cs.columns[y].packages), 1):
                if cs.columns[x].packages[y] is not None:
                    rgb = 240 - (25 * np.digitize(cs.columns[x].packages[y].weight, we_grp))
                    dr_.rectangle(((cord_x, cord_y), (cord_x + 35, cord_y + 35)), fill=(rgb, rgb, rgb), outline='black')
                    dr_.text((cord_x + 5, cord_y + 5), 'ID: %s' % cs.columns[x].packages[y].id, fill='black', font=font)
                    dr_.text((cord_x + 5, cord_y + 20), 'WE: %s' % cs.columns[x].packages[y].weight,
                             fill='black', font=font)
                cord_x += 40
            cord_y -= 40
            cord_x = reset_x

    def _calc_we_dist(self, total_w: int, col_we: int) -> int:
        if total_w == 0 or col_we == 0:
            return 0
        return round((100 * col_we) / total_w)
