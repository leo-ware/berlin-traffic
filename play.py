# import numpy as np
import matplotlib.pyplot as plt
# import networkx as nx
#
# from src.parking_lot import ParkingLot
# from src.on_ramp import OnRamp
# from src.lane import Lane
# from src.network import build_network
# from src.traffic_light import PeriodicAlternatingTrafficLight
#
# from src.dataviz import lane_stats_plot

# build berlin network
# from src.graphs.berlin_map import *
from src.graphs.simple import *


# network = build_network(
#     nodes,
#     edges,
#     entry_points,
#     exit_points,
#     PeriodicAlternatingTrafficLight
# )
#
#
# network.run(1000)
# lane_stats_plot(network, "n_cars")


plt.plot([0, 0.5, 1], [0, 0.5, 1], ls="", marker=".")
plt.show()