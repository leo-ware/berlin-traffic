from src.abstract_asphalt import AbstractAsphalt
from src.exceptions import TooCrowded

import numpy as np


class Lane(AbstractAsphalt):
    def __init__(self, length=100, p_slow=0.1, next: AbstractAsphalt = None, green=True, speed_limit=5):
        """Class that represents a single, unidirectional lane"""
        super().__init__()

        if length < 1:
            raise ValueError("length must be strictly positive")
        if not 0 <= p_slow < 1:
            raise ValueError("p_slow must be on the semi-open interval [0, 1)")
        if not speed_limit > 0:
            raise ValueError("speed_limit must be strictly positive")

        # params
        self.length = length
        self.next = next
        self.green = green
        self.p_slow = p_slow
        self.speed_limit = speed_limit

        # state
        self.speeds = np.array([])
        self.positions = np.array([])

    def n_spaces_available(self):
        """the location of the farthest back car (= number of cars lane can accept)"""
        if len(self.positions):
            return self.positions[0]
        else:
            return self.length

    def space_available(self) -> bool:
        return self.n_spaces_available() > 0

    def blocked(self):
        """whether we should let cars out the end"""
        return self.green and (self.next is None or self.next.space_available())

    def n_queued(self) -> int:
        """Number of cars which are queued at the end of the lane"""
        crushed_pos = np.arange(-len(self.positions), 0) + self.length
        return np.sum(crushed_pos == self.positions)

    def density(self) -> float:
        """Portion of the lane which is full of cars"""
        return len(self.positions) / self.length

    def average_speed(self) -> float:
        """The average speed of cars in the lane"""
        if len(self.positions) == 0:
            return 0
        return np.mean(self.speeds)

    def flow(self) -> float:
        """The flow of the lane"""
        return self.density() * self.average_speed()

    def step(self) -> None:
        """Process one time step of the simulation"""
        if len(self.positions):
            # step 1: acceleration
            self.speeds += 1

            # step 2: slowing down
            backstop = (np.max(self.positions) + self.speed_limit + 1) if self.blocked() else self.length
            space_to_next = np.diff(np.append(self.positions, backstop))
            self.speeds = np.minimum(self.speeds, space_to_next - 1)
            self.speeds = np.minimum(self.speeds, self.speed_limit)

            # step 3: randomization
            self.speeds[np.random.random(len(self.speeds)) < self.p_slow] -= 1
            self.speeds = np.maximum(self.speeds, 0)

            self.positions += self.speeds

            if self.green:
                self.flush()

    def flush(self) -> None:
        """Remove cars which have driven past the end of the lane"""

        flush_from_index = np.searchsorted(self.positions, self.length, side="left")
        flushed_positions = self.positions[flush_from_index:]
        flushed_speeds = self.speeds[flush_from_index:]

        self.positions = self.positions[:flush_from_index]
        self.speeds = self.speeds[:flush_from_index]

        if self.next and len(flushed_positions):
            self.next.push(flushed_positions - self.length, flushed_speeds)

    def push(self, positions, speeds = None) -> None:
        """Add new cars to the beginning of the lane"""

        if len(positions):
            if (speeds is not None) and (len(positions) != len(speeds)):
                raise ValueError("positions and speeds must be same length")

            closest_car = self.n_spaces_available()
            if len(positions) > closest_car:
                print("stuff", len(positions), closest_car)
                raise TooCrowded("no space in lane")

            max_pos = np.arange(len(positions)) + (closest_car - len(positions))
            positions = np.minimum(max_pos, positions)
            positions = np.maximum(positions, 0)

            if speeds is None:
                speeds = np.zeros_like(positions)

            self.positions = np.hstack([positions, self.positions])
            self.speeds = np.hstack([speeds, self.speeds])

    def to_array(self) -> np.array:
        """Generate array representation of the lane"""
        arr = np.zeros(int(self.length))
        arr.put(self.positions.astype(int), 1)
        return arr
