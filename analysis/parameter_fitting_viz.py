import numpy as np
import matplotlib.pyplot as plt

from src.network import avg_across_lanes
from src.dataviz import lane_stats_plot
from src.network import build_network
from src.traffic_light import PeriodicAlternatingTrafficLight
from src.graphs.berlin_map import *

from analysis.theoretical_analysis import adjusted_densities


def speed_comparison(network):
    global google_maps_speeds
    lane_stats_plot(network, "average_speed", normalize=True, show=False, alpha=0.2, label="simulated")
    google_maps_speeds = np.array(google_maps_speeds)
    y = (google_maps_speeds/np.max(google_maps_speeds)).reshape(-1)
    plt.bar(x=np.linspace(0, 1, len(google_maps_speeds)), height=y, width=0.8/len(google_maps_speeds), alpha=0.2, label="real")

    plt.legend()
    plt.show()


def density_comparison(network):

    def d(u, v, lane):
        return lane.density()

    simulated_densities = list(avg_across_lanes(network, d).values())
    simulated_densities /= np.sum(simulated_densities)

    x = np.arange(len(simulated_densities))
    plt.bar(x=x, width=0.8, height=adjusted_densities, label="theoretical density", alpha=0.2)
    plt.bar(x=x, width=0.8, height=simulated_densities, label="simulated density", alpha=0.2)
    plt.ylabel("density (relative)")
    plt.xlabel("lanes")
    plt.xticks([])
    plt.legend()

    plt.show()


if __name__ == "__main__":
    network = build_network(nodes, edges, entry_points, exit_points, PeriodicAlternatingTrafficLight)
    network.run(500)

    speed_comparison(network)
    density_comparison(network)
