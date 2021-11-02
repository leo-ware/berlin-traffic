from src.abstract_asphalt import AbstractAsphalt
from src.warnings import NotConnectedWarning, OneWayError
import numpy as np


class OnRamp(AbstractAsphalt):
    def __init__(self, next=None):
        super().__init__()
        self.next = next

    def step(self):
        if self.next is not None:
            self.next.push(np.array([0]), np.array([0]))
        else:
            raise NotConnectedWarning()

    def push(*_):
        raise OneWayError()
