from src.lane import Lane
from src.abstract_intersection import AbstractIntersection
from src.on_ramp import OnRamp
from src.parking_lot import ParkingLot

import random
import networkx as nx
import matplotlib.pyplot as plt
from itertools import chain
import numpy as np


class Network:
    def __init__(self):
        self.graph = nx.Graph()
        self.lanes = []
        self.on_ramps = []

    # def add_intersection(self, intersection: AbstractIntersection):
    #     self.graph.add_node(intersection)

    def connect(self, a, b, length):
        lane_ab = Lane(next=b, length=length)
        lane_ba = Lane(next=a, length=length)
        self.lanes.extend([lane_ba, lane_ab])
        self.graph.add_edge(a, b, length=length, lanes=[lane_ba, lane_ab])

    def add_entry(self, intersection):
        new = OnRamp(next=intersection)
        self.on_ramps.append(new)
        self.graph.add_edge(intersection, new, length=1)

    def add_exit(self, intersection: AbstractIntersection):
        new = ParkingLot()
        intersection.out_lanes.append(new)
        self.graph.add_edge(intersection, new, length=1)

    def step(self):
        for thing in chain(self.graph.nodes, self.lanes, self.on_ramps):
            thing.step()

    def run(self, n_steps):
        for _ in range(n_steps):
            self.step()

    # statistics
    def edge_densities(self):
        dens = []
        for *_, lanes in self.graph.edges.data("lanes", default=()):
            dens.append(0)
            for lane in lanes:
                dens[-1] += lane.density()/2
        return dens

    # visualization
    def pos(self):
        return nx.kamada_kawai_layout(self.graph, weight="length")

    def node_colors(self):
        cols = []
        for node in self.graph.nodes:
            if isinstance(node, AbstractIntersection):
                cols.append("blue")
            elif isinstance(node, OnRamp):
                cols.append("red")
            else:
                cols.append("black")
        return cols

    def draw_map(self):
        plt.figure(figsize=(10, 10))
        nx.draw(
            self.graph,
            pos=self.pos(),
            with_labels=True,
            node_color=self.node_colors(),
            # edge_cmap=plt.get_cmap("Reds"),
            # edge_vmin=0,
            # edge_vmax=1,
            # edge_color=self.edge_densities()
        )
        plt.show()

    def draw_lanes(self):
        longest_lane = int(max(lane.length for lane in self.lanes))
        lane_views = []
        ticks = []

        plt.figure(figsize=(10, 10))
        for a, b, lanes in self.graph.edges.data("lanes", default=()):
            for name, lane in zip((a, b), lanes):
                ticks.append(name)
                arr = lane.to_array()
                aug = int(longest_lane - len(arr)) * [-1]
                lane_views.append(np.hstack([arr, aug]))
            lane_views.append([-1] * longest_lane)
        plt.imshow(np.vstack(lane_views))
        plt.show()


def build_network(nodes, edges, entry_points, exit_points, intersection_factory):
    network = Network()

    # create intersections
    intersections = {name: intersection_factory(name) for name in nodes}

    # add roads
    for u, v, length in edges:
        a = intersections[u]
        b = intersections[v]
        network.connect(a, b, length*10)

    # create entry & exit points
    for intersection in exit_points:
        network.add_exit(intersections[intersection])

    for intersection in entry_points:
        network.add_entry(intersections[intersection])

    return network


from src.graphs.simple import *
from src.clover_leaf import CloverLeaf

nodes = list("ABCDE")
edges = [
    ["A", "B", 1],
    ["C", "B", 1],
    ["C", "D", 1],
    ["D", "B", 1],
    ["C", "E", 1],
]


network = build_network(
    nodes,
    edges,
    boundary_nodes,
    boundary_nodes,
    CloverLeaf
)

random.seed(123)
np.random.seed(456)

network.run(20)
network.draw_map()

for lane in network.lanes:
    print(lane.to_array())

# network.draw_lanes()