class StopAtStationSummary:
    """Represents changes made in cargo space at the current station."""

    def __init__(self, movements_sum: int, layout_dist: list, weight_dist: list):
        """
        Args:
            movements_sum: total packet movements in the process of loading and unloading.
            layout_dist: number of packets per column
            weight_dist: sum weight of packets per column.
        """

        self.movements_sum = movements_sum
        self.lay_dist = layout_dist
        self.weight_dist = weight_dist
