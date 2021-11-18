import numpy as np
import pygad

from src.network import build_network, avg_across_lanes
from src.traffic_light import PeriodicAlternatingTrafficLight

from src.graphs.berlin_map import nodes, edges, edges_with_data, boundary_points


google_speeds = {}
for u, v, l, s in edges_with_data:
    google_speeds[frozenset([u, v])] = s


def cost_per_lane(u, v, lane):
    if lane:
        obs_value = lane.average_speed()
        exp_value = google_speeds[frozenset([u.name, v.name])]
        return (obs_value - exp_value)**2


def cost(entry_rates, exit_rates, n_steps=500):
    """
    Run the sim with these entry and exit rates and find the MSE between
    simulated average speeds and empirical ones
    """

    entry_dict = {n: float(r) for n, r in zip(boundary_points, entry_rates)}
    exit_dict = {n: int(r) for n, r in zip(boundary_points, exit_rates)}

    network = build_network(nodes, edges, entry_dict, exit_dict, PeriodicAlternatingTrafficLight)
    network.run(n_steps)

    return np.mean(list(avg_across_lanes(network, cost_per_lane).values()))


def pg_fitness(vals, _):
    """Cost function only formatted for genetic optimizer"""
    # these are probabilities
    entry = vals[:len(boundary_points)]
    entry = 1 / entry

    # these are integers
    exit = vals[len(boundary_points):]
    exit = (exit // 1).astype(int)

    return -cost(entry, exit)


def optimize(gens=10):
    ga = pygad.GA(
        # problem specific params
        fitness_func=pg_fitness,
        num_genes=len(boundary_points)*2,
        init_range_low=1,
        init_range_high=10,

        # general optimizer params
        num_generations=gens,
        num_parents_mating=4,
        sol_per_pop=8,
        parent_selection_type="sss",
        keep_parents=1,
        crossover_type="single_point",
        mutation_type="random",
        mutation_percent_genes=10,
    )
    ga.run()
    best = ga.best_solution()
    vals = best[0]

    # convert to usable values
    entry = vals[:len(boundary_points)]
    entry = 1 / entry

    exit = vals[len(boundary_points):]
    exit = (exit // 1).astype(int)

    return entry, exit


if __name__ == "__main__":
    print(optimize())
