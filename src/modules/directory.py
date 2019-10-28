import os
import datetime


class Directory(object):

    """Class manages directories.
    Attributes:
        Class does not have any attributes.
    """

    @staticmethod
    def create() -> str:
        """Creates new directory where results will be saved.
        :return A string, indicating relative path to created folder.
        """
        try:
            path = '../Results/%s' % datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            os.mkdir(path)
            return path
        except OSError as e:
            print(str(e))
            return ''
