from src.abstract_asphalt import AbstractAsphalt
from src.warnings import TooCrowded
import numpy as np


class Lane(AbstractAsphalt):
    def __init__(self, length, p_slow=0.1, next: AbstractAsphalt = None, green=True, speed_limit=5):
        super().__init__()

        # params
        self.length = length
        self.next = next
        self.green = green
        self.p_slow = p_slow
        self.speed_limit = speed_limit

        # state
        self.speeds = np.array([])
        self.positions = np.array([])

    def step(self):
        if len(self.positions):
            # step 1: acceleration
            self.speeds += 1

            # step 2: slowing down
            backstop = (np.max(self.positions) + self.speed_limit + 1) if self.green else self.length
            space_to_next = np.diff(np.append(self.positions, backstop))
            self.speeds = np.minimum(self.speeds, space_to_next - 1)
            self.speeds = np.minimum(self.speeds, self.speed_limit)

            # step 3: randomization
            self.speeds[np.random.random(len(self.speeds)) < self.p_slow] -= 1
            self.speeds = np.maximum(self.speeds, 0)

            self.positions += self.speeds

            if self.green:
                self.flush()

    def flush(self):
        """Remove cars which have driven past the end of the lane"""

        flush_from_index = np.searchsorted(self.positions, self.length, side="left")
        flushed_positions = self.positions[flush_from_index:]
        flushed_speeds = self.speeds[flush_from_index:]

        self.positions = self.positions[:flush_from_index]
        self.speeds = self.speeds[:flush_from_index]

        if self.next and len(flushed_positions):
            self.next.push(flushed_positions - self.length, flushed_speeds)

    def push(self, positions, speeds = None):
        """Add new cars to the beginning of the lane"""

        if len(positions):
            if (speeds is not None) and (len(positions) != len(speeds)):
                raise ValueError("positions and speeds must be same length")

            if len(self.positions):
                closest_car = self.positions[0]
            else:
                closest_car = self.length

            if len(positions) >= closest_car:
                raise TooCrowded("no space in lane")

            max_pos = np.arange(len(positions)) + (closest_car - len(positions))
            positions = np.minimum(max_pos, positions)
            positions = np.maximum(positions, 0)

            if speeds is None:
                speeds = np.zeros_like(positions)

            self.positions = np.hstack([positions, self.positions])
            self.speeds = np.hstack([speeds, self.speeds])
