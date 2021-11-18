import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp

from src.network import build_network, avg_across_lanes
from src.traffic_light import PeriodicAlternatingTrafficLight
from src.dataviz import lane_stats_plot

from src.graphs.berlin_map import nodes, edges, edges_with_data, boundary_points


google_speeds = {}
for u, v, l, s in edges_with_data:
    google_speeds[frozenset([u, v])] = s


def cost_per_lane(u, v, lane):
    if lane:
        obs_value = lane.average_speed()
        exp_value = google_speeds[frozenset([u.name, v.name])]
        return (obs_value - exp_value)**2


def cost(entry_rates, exit_rates):
    entry_dict = {n: float(r) for n, r in zip(boundary_points, entry_rates)}
    exit_dict = {n: int(r) for n, r in zip(boundary_points, exit_rates)}

    network = build_network(nodes, edges, entry_dict, exit_dict, PeriodicAlternatingTrafficLight)
    network.run(500)

    return np.mean(list(avg_across_lanes(network, cost_per_lane).values()))


def optimize():
    n_boundary_points = len(boundary_points)
    entry = cp.Variable(n_boundary_points, nonneg=True)
    exit = cp.Variable(n_boundary_points, integer=True)

    constraints = [
        entry <= 1,
        exit >= 1,
        exit <= 10
    ]

    objective = cp.Minimize(cost(entry, exit))

    prob = cp.Problem(objective, constraints)

    prob.solve()

    print(entry.value)
    print(exit.value)

optimize()


# def plot_solution(entry_rates, exit_rates):
#
# network.run(1000)
# # lane_stats_plot(network, "density", normalize=True)
#
#     lane_stats_plot(network, "average_speed", normalize=True, show=False, alpha=0.2, label="simulated")
#
#     google_maps_speeds = np.array(google_maps_speeds)
#     y = (google_maps_speeds/np.max(google_maps_speeds)).reshape(-1)
#     plt.bar(x=np.linspace(0, 1, len(google_maps_speeds)), height=y, width=0.8/len(google_maps_speeds), alpha=0.2, label="real")
#
#     plt.title("Comparison of simulated and real speeds")
#     plt.legend()
#     plt.show()
