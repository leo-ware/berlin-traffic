from src.abstract_intersection import AbstractIntersection


class CloverLeaf(AbstractIntersection):
    def step(self):
        pass

    def push(self, positions, speeds):
        lanes = self.select_outgoing_lanes(len(positions))
        for i in range(len(self.out_lanes)):
            self.out_lanes[i].push(positions[lanes == i], speeds[lanes == i])
