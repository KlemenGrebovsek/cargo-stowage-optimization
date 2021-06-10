from src.model.dataset import Dataset


class DatasetReaderInterface:

    def read(self, path: str) -> Dataset:
        """Read dataset from file.
        Args:
            path: Path to dataset file.
        Returns: Dataset from file.
        """
        pass
