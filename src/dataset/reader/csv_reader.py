import csv
import os

from src.dataset.reader.dataset_reader_errors import InvalidFileContentError
from src.dataset.reader.ds_reader import DatasetReaderInterface
from src.model.dataset import Dataset
from src.domain.package import Package


class CSVDatasetReader(DatasetReaderInterface):

    def read(self, path: str) -> Dataset:
        """Reads dataset from csv file.

        Throws:
            ValueError, InvalidFileContentError

        Args:
            path: Path to dataset file.

        Returns: Dataset from file.
        """

        if path is None or len(path) < 1 or not os.path.isfile(path):
            raise ValueError('Invalid file path: {0}'.format(path))

        _, extension = os.path.splitext(path)

        if extension != '.csv':
            raise ValueError('Invalid file extension: {0}'.format(extension))

        try:
            with open(path, mode='r') as f:
                reader = csv.reader(f, delimiter=',')
                title = next(reader)
                header = next(reader)

                return Dataset(
                    title=title[0],
                    total_packages=int(header[0]),
                    total_stations=int(header[1]),
                    width=int(header[2]),
                    height=int(header[3]),
                    packages=[Package(int(row[0]), int(row[1]), int(row[2]), int(row[3]))
                              for row in reader]
                )

        except Exception:
            raise InvalidFileContentError('Invalid file content')

