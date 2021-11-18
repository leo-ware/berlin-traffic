from src.lane import Lane
from src.abstract_intersection import AbstractIntersection
from src.clover_leaf import CloverLeaf
from src.on_ramp import OnRamp
from src.parking_lot import ParkingLot

import networkx as nx
import matplotlib.pyplot as plt
from itertools import chain
from typing import List
from collections import defaultdict


class Network:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.lanes: List[Lane] = []
        self.on_ramps: List[OnRamp] = []
        self.parking_lots: List[ParkingLot] = []

    @property
    def intersections(self):
        return [i for i in self.graph.nodes if isinstance(i, AbstractIntersection)]

    def add_road(self, a, b, length):
        lane = Lane(next=b)
        a.out_lanes.append(lane)
        b.in_lanes.append(lane)
        self.lanes.append(lane)
        self.graph.add_edge(a, b, length=length, lane=lane)

    def connect(self, a, b, length):
        self.add_road(a, b, length)
        self.add_road(b, a, length)

    def add_entry(self, intersection, p_join: float = 1):
        new = OnRamp(next=intersection, p=p_join)
        self.on_ramps.append(new)
        self.graph.add_edge(new, intersection, length=1)

    def add_exit(self, intersection: AbstractIntersection, n_exits=1):
        for _ in range(n_exits):
            new = ParkingLot()
            self.parking_lots.append(new)
            intersection.out_lanes.append(new)
            self.graph.add_edge(intersection, new, length=1)

    def wire_intersections(self):
        for u, v, lane in self.graph.edges.data("lane"):
            if isinstance(lane, Lane):
                if isinstance(u, AbstractIntersection):
                    u.out_lanes.append(lane)
                if isinstance(v, AbstractIntersection):
                    v.in_lanes.append(lane)

    def step(self):
        for thing in chain(self.intersections, self.lanes, self.on_ramps):
            thing.step()

    def run(self, n_steps):
        for _ in range(n_steps):
            self.step()

    # visualization
    def pos(self):
        return nx.kamada_kawai_layout(self.graph, weight="length")

    def node_colors(self):
        """Different colors to indicate intersection/on ramp/parking lot"""
        cols = []
        for node in self.graph.nodes:
            if isinstance(node, AbstractIntersection):
                cols.append("blue")
            elif isinstance(node, OnRamp):
                cols.append("red")
            else:
                cols.append("black")
        return cols

    def draw(self):
        """plot a nice little map of the network"""
        plt.figure(figsize=(10, 10))
        nx.draw(self.graph, pos=self.pos(), with_labels=True, node_color=self.node_colors())
        plt.show()


def build_network(nodes, edges, entry_points=None, exit_points=None, intersection_factory=CloverLeaf, distance_scale=10):
    """Builds the networks object from the given description

    Args:
        nodes: list of node names
        edges: list of tuples (intersection_a, intersection_b, street_length)
        entry_points: dict mapping from intersection name to probability of entry per turn
        exit_points: dict mapping from intersection name to number of exits there
        intersection_factory: subclass of AbstractIntersection (default CloverLeaf)
        distance_scale: multiple lengths by this when creating lanes
    """
    network = Network()

    # create intersections
    intersections = {name: intersection_factory(name) for name in nodes}

    # add roads
    for u, v, length in edges:
        a = intersections[u]
        b = intersections[v]
        network.connect(a, b, length*distance_scale)

    # create entry & exit points
    if exit_points:
        for intersection, n in exit_points.items():
            network.add_exit(intersections[intersection], n_exits=n)

    if entry_points:
        for intersection, p in entry_points.items():
            network.add_entry(intersections[intersection], p_join=p)

    return network


def avg_across_lanes(network, func):
    """Calculates a function's average value between incoming and outgoing lanes for every street in the network

    Args:
        network: a Network object
        func: a function which takes two intersections and a lane (in that order) and returns a number
    """
    vals = defaultdict(lambda: 0)
    for u, v, lane in network.graph.edges.data("lane"):
        if lane:
            vals[frozenset([u, v])] += func(u, v, lane)/2
    return dict(vals)
