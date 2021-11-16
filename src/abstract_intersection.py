from abc import ABC
import numpy as np
from src.abstract_asphalt import AbstractAsphalt


class AbstractIntersection(AbstractAsphalt, ABC):
    def __init__(self, name: str = None, in_lanes=(), out_lanes=(), out_rates=None):
        super().__init__()
        if name is None:
            self.name = f"intersection_id#{self._id}"
        else:
            self.name = name

        self.in_lanes = list(in_lanes)
        self.out_lanes = list(out_lanes)
        self._out_rates = out_rates

        if not len(self.out_lanes) == len(self.out_rates):
            raise ValueError("out_lanes and out_rates must be same length")

    def __repr__(self):
        # return f"{self.__class__.__name__}({self.name})"
        return self.name

    def space_available(self) -> bool:
        return False

    @property
    def out_rates(self):
        if self._out_rates is None:
            return np.ones(len(self.out_lanes)) / len(self.out_lanes)
        else:
            return self._out_rates

    def select_outgoing_lanes(self, n_cars):
        """Pick outgoing lanes for cars according to defined likelihoods"""
        if not self.out_lanes:
            raise ValueError("no outgoing lanes")

        try:
            return np.random.choice(
                np.arange(len(self.out_lanes)),
                size=n_cars,
                p=self.out_rates
            )
        except ValueError:
            print("a=", np.arange(len(self.out_lanes)))
            print("p=", self.out_rates)
            raise

    def push(self, positions, speeds):
        lanes = self.select_outgoing_lanes(len(positions))
        for i in range(len(self.out_lanes)):
            self.out_lanes[i].push(positions[lanes == i], speeds[lanes == i])

    def n_queued(self):
        """Number of cars which are queued waiting at the intersection"""
        return sum(lane.n_queued() for lane in self.in_lanes)
