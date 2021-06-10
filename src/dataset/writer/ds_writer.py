from src.model.dataset import Dataset


class DatasetWriterInterface:

    def write(self, dir_path: str, file_name: str, dataset: Dataset):
        """Writes dataset to file.

        Args:
            file_name: Dataset file name without file extension.
            dataset: Dataset to write.
            dir_path: Path to dir.
        Returns: Dataset from file.
        """
        pass
