import os
import unittest

from src.dataset.generator.base_generator import BaseDatasetGenerator
from src.dataset.reader.csv_reader import CSVDatasetReader
from src.dataset.writer.csv_writer import CSVDatasetWriter


def clear_if_exists(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)


class CSVWriterTest(unittest.TestCase):

    def test_invalid_path(self):
        try:
            writer = CSVDatasetWriter()
            generator = BaseDatasetGenerator()
            writer.write('', 'test_empty_path_ds', generator.make('test123', 30, 5, 5))
            self.fail('Empty path error was not thrown.')

        except ValueError:
            pass

    def test_invalid_filename(self):
        try:
            writer = CSVDatasetWriter()
            generator = BaseDatasetGenerator()
            writer.write('../../resource/', '', generator.make('test123', 30, 5, 5))
            self.fail('Empty path error was not thrown.')

        except ValueError:
            pass

    def test_valid_path_filename(self):
        try:
            writer = CSVDatasetWriter()
            generator = BaseDatasetGenerator()
            writer.write('../../resource/', 'test_valid_path_filename', generator.make('test123', 30, 5, 5))

        except ValueError as e:
            self.fail(e)
        finally:
            clear_if_exists('../../resource/test_valid_path_filename.csv')

    def test_duplicate_file(self):
        try:
            writer = CSVDatasetWriter()
            generator = BaseDatasetGenerator()
            dataset = generator.make('test123', 30, 5, 5)
            writer.write('../../resource/', 'test_duplicate_file', dataset)
            writer.write('../../resource/', 'test_duplicate_file', dataset)
            self.fail('Duplicate file exception was not thrown')

        except ValueError:
            pass
        finally:
            clear_if_exists('../../resource/test_duplicate_file.csv')

    def test_file_content(self):
        try:
            writer = CSVDatasetWriter()
            reader = CSVDatasetReader()
            generator = BaseDatasetGenerator()
            dataset = generator.make('test123', 30, 5, 5)
            writer.write('../../resource/', 'test_file_content', dataset)
            new_dataset = reader.read('../../resource/test_file_content.csv')
            is_valid = True

            if dataset.title != new_dataset.title:
                is_valid = False

            if dataset.total_packages != new_dataset.total_packages:
                is_valid = False

            if dataset.total_stations != new_dataset.total_stations:
                is_valid = False

            if dataset.width != new_dataset.width or dataset.height != new_dataset.height:
                is_valid = False

            if len(dataset.packages) != len(new_dataset.packages):
                is_valid = False

            self.assertEqual(True, is_valid)

        except ValueError as e:
            self.fail(e)
        finally:
            clear_if_exists('../../resource/test_file_content.csv')
