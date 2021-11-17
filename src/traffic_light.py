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

    def get_index_green(self):
        """Returns the index of the lane which is currently green"""
        return self._index_green

    def set_index_green(self, index):
        """Sets the index of the lane which is currently green"""
        if self._index_green is not None:
            self.in_lanes[self._index_green].green = False
        self.in_lanes[index].green = True
        self._index_green = index

    @abstractmethod
    def n_step(self):
        """Update method called every n-steps"""
        pass

    def step(self):
        self.counter += 1
        if self.counter % self.period == 0:
            self.n_step()


class PeriodicAlternatingTrafficLight(AbstractTrafficLight):
    """Periodic traffic light that alternates between lanes"""
    def n_step(self):
        if len(self.in_lanes):
            if self.get_index_green() is None:
                self.set_index_green(0)
            else:
                new_green = (self.get_index_green() + 1) % len(self.in_lanes)
                self.set_index_green(new_green)


class PeriodicRandomTrafficLight(AbstractTrafficLight):
    """Periodic traffic light that picks a random lane"""
    def n_step(self):
        if len(self.in_lanes):
            new_green = random.randrange(len(self.in_lanes))
            self.set_index_green(new_green)


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
                self.set_index_green(best_i)
