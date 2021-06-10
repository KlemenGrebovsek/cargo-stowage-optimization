import unittest

from src.dataset.reader.csv_reader import CSVDatasetReader


class CSVReaderTest(unittest.TestCase):
    def test_empty_path(self):
        try:
            reader = CSVDatasetReader()
            _ = reader.read('')
            self.fail('Empty path should not be accepted')
        except ValueError:
            pass

    def test_invalid_path(self):
        try:
            reader = CSVDatasetReader()
            _ = reader.read('./random/dataset.csv')
            self.fail('Invalid path should not be accepted')
        except ValueError:
            pass

    def test_valid_path(self):
        try:
            reader = CSVDatasetReader()
            _ = reader.read('../../resource/testSet.csv')
        except ValueError:
            self.fail('Valid path should be accepted')

    def test_invalid_file_extension(self):
        try:
            reader = CSVDatasetReader()
            _ = reader.read('./random/dataset.txt')
            self.fail('Invalid file extension should not be accepted')
        except ValueError:
            pass

    def test_valid_file_extension(self):
        try:
            reader = CSVDatasetReader()
            _ = reader.read('../../resource/testSet.csv')
        except ValueError:
            self.fail('Valid file extension should be accepted')

    def test_invalid_file(self):
        try:
            reader = CSVDatasetReader()
            _ = reader.read('../../resource/invalidTestSet.csv')
            self.fail('Invalid dataset should not be accepted')
        except ValueError:
            pass

    def test_valid_file_value(self):
        try:
            reader = CSVDatasetReader()
            dataset = reader.read('../../resource/testSet.csv')
            is_valid = True

            if dataset.title != 'TestSet1':
                is_valid = False

            if dataset.total_packages != 120:
                is_valid = False

            if dataset.total_stations != 6:
                is_valid = False

            if dataset.width != 15 or dataset.height != 15:
                is_valid = False

            if len(dataset.packages) != 120:
                is_valid = False

            self.assertEqual(True, is_valid)
        except ValueError as e:
            self.fail(e)
