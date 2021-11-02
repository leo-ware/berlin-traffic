from abc import ABC
import numpy as np
from src.abstract_asphalt import AbstractAsphalt


class AbstractIntersection(AbstractAsphalt, ABC):
    def __init__(self, in_lanes=(), out_lanes=(), out_rates=None):
        super().__init__()
        self.in_lanes = list(in_lanes)
        self.out_lanes = list(out_lanes)

        if out_rates is None:
            self.out_rates = np.ones(len(out_lanes)) / len(out_lanes)
        else:
            self.out_rates = out_rates

        if not len(self.out_lanes) == len(self.out_rates):
            raise ValueError("out_lanes and out_rates must be same length")

    def select_outgoing_lanes(self, n_cars):
        """Pick outgoing lanes for cars according to defined likelihoods"""
        if not self.out_lanes:
            raise ValueError("no outgoing lanes")

        return np.random.choice(
            np.arange(len(self.out_lanes)),
            size=n_cars,
            p=self.out_rates
        )

    def push(self, positions, speeds):
        lanes = self.select_outgoing_lanes(len(positions))
        for i in range(len(self.out_lanes)):
            self.out_lanes[i].push(positions[lanes == i], speeds[lanes == i])
