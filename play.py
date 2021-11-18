import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from src.parking_lot import ParkingLot
from src.on_ramp import OnRamp
from src.lane import Lane
from src.network import build_network
from src.traffic_light import PeriodicAlternatingTrafficLight

from src.dataviz import lane_stats_plot

# from src.graphs.simple import *
from src.graphs.berlin_map import *

network = build_network(
    nodes,
    edges,
    entry_points,
    exit_points,
    PeriodicAlternatingTrafficLight
)


network.run(1000)
lane_stats_plot(network, "average_speed", normalize=True, show=False, alpha=0.2, label="simulated")

google_maps_speeds = np.array(google_maps_speeds)
y = (google_maps_speeds/np.max(google_maps_speeds)).reshape(-1)
plt.bar(x=np.linspace(0, 1, len(google_maps_speeds)), height=y, width=0.8/len(google_maps_speeds), alpha=0.2, label="real")

plt.legend()
plt.show()
