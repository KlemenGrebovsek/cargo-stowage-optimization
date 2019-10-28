from PIL import Image, ImageDraw, ImageFont
import numpy as np
import imageio
from src.main_classes.simulation_settings import SimulationSettings
from src.main_classes.cargo_space import CargoSpace


class ImageViz(object):

    """Class manages visualization for best solution.
    Attributes:
        Class does not have any attributes.
    """

    @staticmethod
    def viz_best_sol(sim_sett: SimulationSettings, path: str, res: list):
        """Saves gif for best solution, which contains pictures of cargo space at each station.
         :param sim_sett: An object, indicating optimization settings.
         :param path: A string, representing relative path of save folder.
         :param res: A List, containing results of simulation.
        """

        best_sol = min(res, key=lambda x: x[1])
        print('Saving best solution visualization in %s.gif' % best_sol[0])
        img_arr = ImageViz._simulate_route(sim_sett, best_sol)
        imageio.mimsave('%s/%s.gif' % (path, best_sol[0]), img_arr, fps=55, loop=0, duration=4)

    @staticmethod
    def _simulate_route(sim_sett: SimulationSettings, res: list) -> list:
        """ Simulates route of the ship and generates images of cargo space status at every station.
        :param sim_sett: An object, indicating optimization settings.
        :param res: A List, containing results of simulation.
        :return A List of images, each image visualizes cargo space at specific station.
        """

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
            stat_image = Image.new('RGB', ((sim_sett.cs_width * 75) + (5 * sim_sett.cs_width) + 30,
                                           ((sim_sett.cs_height * 35) + 50)), color='white')
            draw_obj = ImageDraw.Draw(stat_image)
            x, y = 5, stat_image.height - 65
            x_line = x + (35 * sim_sett.cs_width) + (5 * sim_sett.cs_width) + 10
            draw_obj.text((x, 15), 'Station number: %s' % station, fill='black',
                          font=ImageFont.truetype('arial.ttf', 20))
            draw_obj.text((x, 50), 'Cargo space before station', fill='black', font=ImageFont.truetype('arial.ttf', 20))
            draw_obj.line(((x_line, y + 35), (x_line, y - (25 * sim_sett.cs_height))), fill=50, width=2)
            ImageViz._draw_cs(draw_obj, cargo_space, x, y, ImageFont.truetype('arial.ttf', 8), col_we_sum, we_gr)
            dr_x = 30 + (35 * sim_sett.cs_width) + (5 * sim_sett.cs_width)
            dr_y = stat_image.height - 65
            draw_obj.text((dr_x, 50), 'Cargo space after station', fill='black',
                          font=ImageFont.truetype('arial.ttf', 20))

            m, l, col_we_sum = cargo_space.simulate_stop_at_station(station, sim_sett.packages_by_station[station - 1])

            ImageViz._draw_cs(draw_obj, cargo_space, dr_x, dr_y, ImageFont.truetype('arial.ttf', 8), col_we_sum, we_gr)
            img_arr.append(stat_image)
        return img_arr

    @staticmethod
    def _draw_cs(dr_: ImageDraw, cs: CargoSpace, cord_x: int, cord_y: int, font: ImageFont, col_w: list, we_grp: tuple):
        """Draws a storage space on an image.
        :param dr_: A ImageDraw, representing object responsible fro drawing.
        :param cs: A List[List], representing cargo space.
        :param cord_x: An Integer, representing x coordinate for drawing object.
        :param cord_y: An Integer, representing y coordinate for drawing object.
        :param font: A ImageFont, specifies font on image.
        :param col_w: An Integer, representing height of a cargo storage column.
        :param we_grp: A Tuple representing the distribution of the weight of packets into classes.
        """

        reset_x = cord_x
        cs_sum_we = sum(col_w)

        for f in range(0, len(cs.columns), 1):
            dr_.text((cord_x + 12, cord_y + 43), '%s%%' % ImageViz._calc_we_dist(cs_sum_we, col_w[f]), fill='black')
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

    @staticmethod
    def _calc_we_dist(total_w: int, col_we: int) -> int:
        """A helper method for cargo space visualization, returns selected column weight in percentage.
        :param total_w: An Integer, representing a sum weight of cargo space.
        :param col_we: An Integer, representing a weight of a selected column in cargo space.
        :return An integer representing the weight of the column as a percentage of the weight of the storage space.
        """

        if total_w == 0 or col_we == 0:
            return 0
        return round((100 * col_we) / total_w)
