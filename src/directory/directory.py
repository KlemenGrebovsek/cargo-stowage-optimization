import os
import datetime


class Directory(object):

    @staticmethod
    def create(path: str) -> str:
        """
        :param path: Path of dir, where new folder will be created.
        :return: Path to created folder.
        """
        try:
            path = '%s/%s' % (path, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            os.mkdir(path)
            return path

        except OSError as e:
            print('OSError: ' + str(e))
            return ''
