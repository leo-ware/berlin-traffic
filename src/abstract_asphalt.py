from abc import ABC, abstractmethod
import numpy as np


class AbstractAsphalt(ABC):
    n_items = 0

    def __init__(self):
        self._id = AbstractAsphalt.n_items
        AbstractAsphalt.n_items += 1

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} _id={self._id}>"

    def __hash__(self) -> int:
        return hash(str(self))

    # def __eq__(self, other):
    #     return isinstance(other, AbstractAsphalt) and (str(self) == str(other))

    @abstractmethod
    def push(self, positions: np.array, speeds: np.array) -> None:
        """add cars with the given positions and speeds"""
        pass

    @abstractmethod
    def step(self) -> None:
        """state update for one time-step of the model"""
        pass

    @abstractmethod
    def space_available(self) -> bool:
        """whether one additional car can be accepted"""
        pass
