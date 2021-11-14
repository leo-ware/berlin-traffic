from src.abstract_asphalt import AbstractAsphalt
from src.warnings import NoOutlet, OneWayError
import numpy as np
import random


class OnRamp(AbstractAsphalt):
    def __init__(self, next=None, p=1):
        """Generates a car each step with probability p"""
        super().__init__()
        self.p = p
        self.next = next

    def __repr__(self):
        return "<>"

    def step(self):
        if self.next is None:
            raise NoOutlet()
        elif random.random() < self.p:
            self.next.push(np.array([0]), np.array([0]))

    def push(*_):
        raise OneWayError()
