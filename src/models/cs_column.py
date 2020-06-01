from src.models.package import Package


class Column(object):

    def __init__(self, cs_height: int):
        self.packages = [None for i in range(cs_height)]
        self.package_count = 0
        self.weight = 0

    def get_size(self) -> int:
        return len(self.packages)

    def push(self, package: Package):
        self.packages[self.package_count] = package
        self.package_count += 1
        self.weight += package.weight

    def pop(self) -> object:
        self.package_count -= 1
        self.weight -= self.packages[self.package_count].weight
        return self.packages[self.package_count]

    def unload_at_station(self, station_index: int) -> tuple:
        wait_que, mov_sum, wait_que_act = [], 0, False

        for i in range(self.package_count):
            if wait_que_act:
                self.package_count -= 1
                self.weight -= self.packages[i].weight
                wait_que.append(self.packages[i])
                self.packages[i] = None
                mov_sum += 1
                continue
            elif self.packages[i].station_out == station_index:
                self.package_count -= 1
                self.weight -= self.packages[i].weight
                self.packages[i] = None
                wait_que_act = True
                mov_sum += 1

        return wait_que, mov_sum
