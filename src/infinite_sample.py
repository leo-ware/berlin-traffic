import numpy as np


class InfiniteSample:
    def __init__(self, vals, dist):
        if not vals:
            raise ValueError("vals and dist must have at least one element")

        self.vals = list(vals)
        self.dist = np.array(dist)/np.sum(dist)
        self.next = self.sample()

        if len(self.vals) != len(self.dist):
            raise ValueError("vals and dist must be same length")

    def sample(self):
        return np.random.choice(a=self.vals, p=self.dist)

    def peak(self):
        return self.next

    def pop(self):
        val = self.next
        self.next = self.sample()
        return val
