from abc import ABC
import numpy as np

from src.abstract_asphalt import AbstractAsphalt
from src.infinite_sample import InfiniteSample


class AbstractIntersection(AbstractAsphalt, ABC):
    def __init__(self, name: str = None, in_lanes=(), out_lanes=(), out_rates=None):
        super().__init__()

        if name is None:
            self.name = f"intersection_id#{self._id}"
        else:
            self.name = name

        self.in_lanes = list(in_lanes)
        self.out_lanes = list(out_lanes)
        self.out_rates = out_rates
        self.assignments = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"
        # return self.name

    def setup(self):
        """function must be run before first step"""
        if self.out_rates is None:
            self.out_rates = np.ones(len(self.out_lanes)) / len(self.out_lanes)
        elif len(self.out_lanes) != len(self.out_rates):
            ValueError("out_lanes and out_rates must be same length")

        # freeze in/out lanes
        self.in_lanes = tuple(self.in_lanes)
        self.out_lanes = tuple(self.out_lanes)

        self.assignments = InfiniteSample(self.out_lanes, self.out_rates)

    def space_available(self) -> bool:
        if self.assignments is None:
            self.setup()
        return self.assignments.peak().space_available()

    # def select_outgoing_lanes(self, n_cars):
    #     """Pick outgoing lanes for cars according to defined likelihoods"""
    #     if self.assignments is None:
    #         self.setup()
    #     return np.array([self.assignments.pop() for _ in range(n_cars)])

    def push(self, positions, speeds):
        for p, s in zip(positions, speeds):
            self.assignments.pop().push([p], [s])

    def n_queued(self):
        """Number of cars which are queued waiting at the intersection"""
        return sum(lane.n_queued() for lane in self.in_lanes)
