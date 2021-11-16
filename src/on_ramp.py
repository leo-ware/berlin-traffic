from src.abstract_asphalt import AbstractAsphalt
from src.exceptions import NoOutlet, OneWayError
import numpy as np
import random


class OnRamp(AbstractAsphalt):
    def __init__(self, next: AbstractAsphalt = None, p=1):
        """Generates a car each step with probability p"""
        super().__init__()
        self.p = p
        self.next = next
        self.blocks = 0

    def __repr__(self):
        return "<>"

    def step(self):
        if self.next is None:
            raise NoOutlet()
        elif random.random() < self.p:
            if self.next.space_available():
                self.next.push(np.array([0]), np.array([0]))
            else:
                self.blocks += 1

    def space_available(self) -> bool:
        return False

    def push(*_):
        raise OneWayError()
