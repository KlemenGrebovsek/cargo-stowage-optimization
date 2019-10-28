from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from textwrap import wrap


class Graph(object):

    """Class manages drawing of a graphs.
    Attributes:
        Class does not have any attributes.
    """

    @staticmethod
    def save_graph(results: list, path: str):
        """Generates and saves a graph containing a comparison of fitness values ​​and runtime of algorithms.
        :param results: A list, indicating results of optimization with EA.
        :param path: A string, indicating relative path of save folder.
        """

        try:
            print('Saving graph in graph.png')
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
            plt.savefig('%s/graph.png' % path)
        except Exception as e:
            print(str(e))
