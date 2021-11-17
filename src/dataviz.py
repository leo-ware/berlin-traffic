import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import numpy as np
import networkx as nx
from collections import defaultdict

from src.graphs.simple import *
from src.network import build_network


def space_time_plot(hist):
    """Takes the history of a lane and generates a space-time plot

    Args:
        hist: a list of arrays, where each array comes from a Lane.to_array() call
    """
    step_numbers = []
    positions = []

    for step, arr in enumerate(hist):
        pos = np.nonzero(arr)
        stp = np.zeros_like(pos)
        stp.fill(step)

        positions.append(pos)
        step_numbers.append(stp)

    positions = np.hstack(positions)
    step_numbers = np.hstack(step_numbers)

    plt.scatter(positions, step_numbers, s=1, c="black")
    plt.ylabel("timestep")
    plt.xlabel("position")
    plt.show()


def lane_stats_plot(network, attr="average_speed"):
    vals_dict = defaultdict(lambda: 0)
    for u, v, lane in network.graph.edges.data("lane"):
        if lane:
            vals_dict[frozenset([u, v])] += getattr(lane, attr)()/2

    names = np.array([str(name) for name in vals_dict])
    vals = np.array(list(vals_dict.values()))
    x = np.linspace(0, 1, len(vals))

    plt.bar(x, vals, tick_label=names, width=0.8/vals.size)
    plt.xticks(rotation=90)
    plt.show()


def translate(vals, x1, y1, x2, y2):
    """translates a 1d array of values into 2d"""

    vals_sum = np.sum(vals)
    if vals_sum:
        vals /= vals_sum

    dx = x2 - x1
    dy = y2 - y1

    x_vals = (dx * vals) + x1
    y_vals = (dy * vals) + y1

    return x_vals, y_vals


def draw_cars(network):
    """draw map of all traffic with cars represented by dots"""
    pos = network.pos()

    # plot intersections
    nodes_plot = nx.draw_networkx_nodes(network.graph, pos, nodelist=network.intersections, node_color="red", node_size=10)
    names = {node: node.name for node in network.intersections}
    # labels_plot = nx.draw_networkx_labels(network.graph, pos, labels=names, horizontalalignment="left", verticalalignment="top")

    # plot traffic
    plots = [nodes_plot]
    for u, v, lane in network.graph.edges.data("lane"):
        if lane:
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            cars = lane.to_array()
            cars_2d = translate(cars, x1, y1, x2, y2)
            plot = plt.plot(*cars_2d, ls="", marker=".", c="black", animated=True)
            plots.append(plot[0])

    return plots


network = build_network(nodes, edges, entry_points, exit_points)

# push fake car data
for lane in network.lanes:
    lane.push([1, 5, 6, 8])

# draw_cars(network)

fig = plt.figure()
frames = []
for _ in range(10):
    network.step()
    frames.append(draw_cars(network))

anim = ArtistAnimation(fig, artists=frames, blit=True, interval=50)
anim.save("../imgs/foo.gif")
