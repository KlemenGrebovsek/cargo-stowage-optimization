import unittest

from src.dataset.generator.base_generator import BaseDatasetGenerator


class BaseGeneratorTest(unittest.TestCase):

    def test_none_title(self):
        generator = BaseDatasetGenerator()
        try:
            _ = generator.make(None, 30, 5, 5)
            self.fail()
        except ValueError:
            pass

    def test_empty_title(self):
        generator = BaseDatasetGenerator()
        try:
            _ = generator.make('', 30, 5, 5)
            self.fail()
        except ValueError:
            pass

    def test_valid_title(self):
        generator = BaseDatasetGenerator()
        try:
            dataset = generator.make('test123', 30, 5, 5)
            self.assertEqual('test123', dataset.title)
        except ValueError as e:
            self.fail(e)

    def test_invalid_station_number(self):
        generator = BaseDatasetGenerator()
        try:
            _ = generator.make('test123', 30, 2, 5)
            self.fail()
        except ValueError:
            pass

    def test_valid_station_number(self):
        generator = BaseDatasetGenerator()
        try:
            dataset = generator.make('test123', 30, 5, 5)
            self.assertEqual('test123', dataset.title)
        except ValueError as e:
            self.fail(e)

    def test_invalid_dimension_number(self):
        generator = BaseDatasetGenerator()
        try:
            _ = generator.make('test123', 30, 5, 2)
            self.fail()
        except ValueError:
            pass

    def test_valid_dimension_number(self):
        generator = BaseDatasetGenerator()
        try:
            dataset = generator.make('test123', 30, 5, 5)
            self.assertEqual('test123', dataset.title)
        except ValueError as e:
            self.fail(e)

    def test_invalid_package_number(self):
        generator = BaseDatasetGenerator()
        try:
            _ = generator.make('test123', 7, 5, 2)
            self.fail()
        except ValueError:
            pass

    def test_valid_package_number(self):
        generator = BaseDatasetGenerator()
        try:
            dataset = generator.make('test123', 30, 5, 5)
            self.assertEqual('test123', dataset.title)
        except ValueError as e:
            self.fail(e)

    def test_to_small_cargo_space(self):
        generator = BaseDatasetGenerator()
        try:
            _ = generator.make('', 100, 5, 5)
            self.fail()
        except ValueError:
            pass

    def test_valid_in_out_station(self):
        generator = BaseDatasetGenerator()
        try:
            dataset = generator.make('test123', 54, 5, 5)

            for package in dataset.packages:
                if package.station_in >= package.station_out:
                    self.fail('Invalid package route attributes.')
        except ValueError as e:
            self.fail(e)
