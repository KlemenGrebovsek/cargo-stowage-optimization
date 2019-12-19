import random
import csv
import datetime
from src.main_classes.package import Package
from src.main_classes.simulation_settings import SimulationSettings


class File(object):

    """ Class generates and reads files so-called "data sets" and parses them into specific structures. It also includes
     a method which saved optimization results in txt file.
    Attributes:
        Class does not have any attributes.
    """

    @staticmethod
    def generate_new_data_set(ds_name: str, pack_c: int, stat_n: int, cargo_s_w: int, cargo_s_h: int) -> str:
        """ Creates a new data set in the form of a csv file. The data set is designed according to the specifications
        given.
        :param ds_name: A string, indicating data set name.
        :param pack_c: An integer, indicating number of total packages.
        :param stat_n: An integer, indicating number of stations.
        :param cargo_s_w: An integer, indicating cargo space width.
        :param cargo_s_h: An integer, indicating cargo space height.
        :return A tuple that describes the success of generating a data set, or an error that occurs.
        """

        err_list = []
        # Check if any logical errors.
        if not isinstance(ds_name, str):
            err_list.append('Data set name must be a string.')
        if not all(isinstance(element, int) for element in range(1, 5, 1)):
            err_list.append('Data set specifications must be an integer.')
        if stat_n < 5:
            err_list.append('Minimum number of stations is 5.')
        if cargo_s_h != cargo_s_w:
            err_list.append('Cargo space width and height must be the same.')
        if pack_c < 30:
            err_list.append('Minimum number of packages is 30.')
        if ((pack_c * 8) / 10) - 1 > cargo_s_w * cargo_s_h:
            err_list.append('Cargo space dimensions are too small.')

        if err_list:
            return ','.join(err_list)

        try:
            with open("../Datasets/%s.csv" % ds_name, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([pack_c, stat_n, cargo_s_w, cargo_s_h])
                for packageCounter in range(1, int(pack_c) + 1, 1):
                    st_out = random.randint(2, int(stat_n))
                    writer.writerow([packageCounter, random.randint(1, st_out - 1), st_out, random.randint(1, 99)])
        except IOError as ioe:
            return 'IO exception : %s.' % str(ioe)
        except Exception as e:
            return str(e)
        return 'Done!'

    @staticmethod
    def read_data_set(ds_name: str) -> tuple:
        """Reads dataset from a csv file and parses data into specific structures.
        :param ds_name: A string, indicating data set name.
        :return A tuple (SimulationSettings, Error)
        """

        print('Reading data set.')
        try:
            with open('../Datasets/%s.csv' % ds_name, mode='r') as f:
                reader = csv.reader(f, delimiter=',')
                header = next(reader)
                pack_c, stat_n, car_pac_wi, car_spa_he = int(header[0]), int(header[1]), int(header[2]), int(header[3])
                packages = [[] for x in range(stat_n)]
                for row in reader:
                    packages[int(row[1]) - 1].append(Package(int(row[0]), int(row[2]), int(row[3])))
            if pack_c != sum(len(i) for i in packages):
                return SimulationSettings(0, 0, 0, 0, 0, ' '), 'Dataset validation failed.'
        except IOError:
            print('Dataset %s does not exists.' % ds_name)
        except Exception as ex:
            return SimulationSettings(0, 0, 0, 0, 0, ' '), 'Unexpected error: %s' % str(ex)

        return SimulationSettings(pack_c, packages, stat_n, car_pac_wi, car_pac_wi, ds_name), None

    @staticmethod
    def save_to_txt(path: str, res: list, np: int, n_fes: int, sim_settings: SimulationSettings):
        """Saves optimization settings and results into txt file.
         :param path: A string, indicating relative path of save folder.
         :param res: A list, indicating results of optimization with EA.
         :param np: An integer, indicating population size.
         :param n_fes: An integer, indicating number of evaluations per algorithm.
         :param sim_settings: An object, indicating optimization settings.
        """

        print('Saving results in simInfo.txt.')
        try:
            with open('%s/simInfo.txt' % path, 'w') as wr:
                wr.write('----Optimization info---- \n')
                wr.write('Date: %s \n' % datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
                wr.write('Algorithms: %s \n \n' % len(res))
                wr.write('----Dataset info---- \n')
                wr.write('Name : %s \n' % sim_settings.ds_name)
                wr.write('Number of packages : %s \n' % sim_settings.pack_count)
                wr.write('Number of stations : %s \n' % sim_settings.station_n)
                wr.write('Cargo stowage size : %sx%s \n \n' % (sim_settings.cs_width, sim_settings.cs_height))
                wr.write('----EA properties----\n')
                wr.write('Population size : %s \n' % np)
                wr.write('Number of evaluations : %s \n \n' % n_fes)
                wr.write('----Optimization results---- \n')
                for result in res:
                    wr.write('%s, Fitness: %s, ExecutionTime : %s sec \n' % (result[0], result[1], round(result[3], 5)))
        except IOError as ioe:
            print('IO exception : %s.' % str(ioe))
        except Exception as e:
            print('Other exception: %s' % str(e))
