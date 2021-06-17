import unittest

from src.dataset.reader.csv_reader import CSVDatasetReader
from src.dataset.reader.dataset_reader_errors import InvalidFileContentError


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

    def test_invalid_content(self):
        try:
            reader = CSVDatasetReader()
            _ = reader.read('../../resource/invalidTestSet.csv')
            self.fail('Invalid dataset should not be accepted')
        except InvalidFileContentError:
            pass

    def test_empty_content(self):
        try:
            reader = CSVDatasetReader()
            _ = reader.read('../../resource/emptyFile.csv')
            self.fail('Invalid dataset should not be accepted')
        except InvalidFileContentError:
            pass

    def test_valid_content(self):
        try:
            reader = CSVDatasetReader()
            dataset = reader.read('../../resource/testSet.csv')

            self.assertEqual('TestSet1', dataset.title)
            self.assertEqual(120, dataset.total_packages)
            self.assertEqual(6, dataset.total_stations)
            self.assertEqual(15, dataset.width)
            self.assertEqual(15, dataset.height)

        except Exception as e:
            self.fail(e)
