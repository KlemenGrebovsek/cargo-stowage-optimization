from src.model.dataset import Dataset


class DatasetGeneratorInterface:

    def make(self, ds_name: str, pack_c: int, stat_n: int, cargo_dim: int) -> Dataset:
        """Generates new dataset.

        Args:
            ds_name: Data set name, without file extension.
            pack_c: Total number of packages.
            stat_n: Total number of stations.
            cargo_dim: Cargo stowage space width and height.
        Returns: Generated dataset.
        """
        pass
