import csv
import os

from src.dataset.writer.ds_writer import DatasetWriterInterface
from src.model.dataset import Dataset


class CSVDatasetWriter(DatasetWriterInterface):

    def write(self, dir_path: str, file_name: str, dataset: Dataset):
        """Writes dataset to csv file.

        Args:
            file_name: Dataset file name without file extension.
            dataset: Dataset to write.
            dir_path: Path to dir.
        Returns: Dataset from file.
        """

        if dir_path is None or len(dir_path) < 1 or not os.path.isdir(dir_path):
            raise ValueError('Invalid dir path')

        if file_name is None or len(file_name) < 1:
            raise ValueError('Invalid file name')

        full_path = os.path.join(dir_path, file_name+'.csv')

        if os.path.isfile(full_path):
            raise ValueError('File already exists')

        with open(full_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([dataset.title])

            writer.writerow([dataset.total_packages,
                             dataset.total_stations,
                             dataset.width,
                             dataset.height])

            for package in dataset.packages:
                writer.writerow([package.id, package.station_in, package.station_out, package.weight])
