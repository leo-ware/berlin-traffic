from abc import ABC, abstractmethod
from src.intersections.abstract_intersection import AbstractIntersection


class AbstractTrafficLight(AbstractIntersection, ABC):
    def __init__(self, in_lanes=(), out_lanes=(), out_rates=None, period=10):
        super().__init__(in_lanes, out_lanes, out_rates)

        if period <= 0:
            raise ValueError("period must be positive")

        self.period = period
        self.counter = 0

        self._index_green = None
        for lane in self.in_lanes:
            lane.green = False

    @property
    def index_green(self):
        return self._index_green

    @index_green.setter
    def index_green(self, index):
        if self._index_green is not None:
            self.in_lanes[self._index_green].green = False
        self.in_lanes[index].green = True
        self._index_green = index

    @abstractmethod
    def n_step(self):
        pass

    def step(self):
        self.counter += 1
        if self.counter % self.period == 0:
            self.n_step()


class PeriodicTrafficLight(AbstractTrafficLight):
    def n_step(self):
        self.index_green = (self.index_green + 1) % len(self.out_lanes)


class PeriodicAdaptiveTrafficLight(AbstractTrafficLight):
    def n_step(self):
        best_index = max(range(len(self.out_lanes)), key=lambda i: len(self.out_lanes[i].positions))
        self.index_green = best_index
