from abc import ABC, abstractmethod
import random
from src.abstract_intersection import AbstractIntersection


class AbstractTrafficLight(AbstractIntersection, ABC):
    def __init__(self, *args, period=10, **kwargs):
        super().__init__(*args, **kwargs)

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


class PeriodicAlternatingTrafficLight(AbstractTrafficLight):
    """Periodic traffic light that alternates between lanes"""
    def n_step(self):
        if len(self.in_lanes):
            if self.index_green is None:
                self.index_green = 0
            else:
                self.index_green = (self.index_green + 1) % len(self.in_lanes)


class PeriodicRandomTrafficLight(AbstractTrafficLight):
    """Periodic traffic light that picks a random lane"""
    def n_step(self):
        if len(self.in_lanes):
            self.index_green = random.randrange(len(self.in_lanes))


class PeriodicAdaptiveTrafficLight(AbstractTrafficLight):
    """Periodic traffic light that always picks the lane with the most queued cars"""
    def n_step(self):
        if len(self.in_lanes):

            best_i = None
            longest_queue = float("-inf")
            for i, lane in enumerate(self.in_lanes):
                queue = lane.n_queued()
                if queue > longest_queue:
                    longest_queue = queue
                    best_i = i

            if best_i is not None:
                self.index_green = best_i
