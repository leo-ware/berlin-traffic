import numpy as np
import matplotlib.pyplot as plt

from src.network import build_network, avg_across_lanes
from src.traffic_light import PeriodicAdaptiveTrafficLight, PeriodicAlternatingTrafficLight, PeriodicRandomTrafficLight
from src.clover_leaf import CloverLeaf

from src.graphs.berlin_map import *


def make_plots(n_boots=100, n_steps=500):
    intersection_options = [
        CloverLeaf,
        PeriodicAlternatingTrafficLight,
        PeriodicRandomTrafficLight,
        PeriodicAdaptiveTrafficLight
    ]

    # track stats for each intersection type
    intersection_avgs = {}
    intersection_highs = {}
    intersection_lows = {}

    # matplotlib initialization for each kind of plot
    hist_cmp_fig, hist_cmp_ax = plt.subplots(1, 1, figsize=(10, 5))
    mean_cmp_fig, mean_cmp_ax = plt.subplots(1, 1, figsize=(10, 5))
    multifig, multiaxes = plt.subplots(2, 2, figsize=(10, 6))

    for intersection_factory, ax in zip(intersection_options, multiaxes.flatten()):

        # run the model and collect data
        avg_speeds_runs = []
        for run in range(n_boots):
            network = build_network(nodes, edges, entry_points, exit_points, intersection_factory)
            network.run(n_steps)
            avg_speeds = np.array(list(avg_across_lanes(network, lambda u, v, lane: lane.average_speed()).values()))
            avg_speeds_runs.append(avg_speeds)
        avg_speeds_runs = np.vstack(avg_speeds_runs)

        # mean and 95% confidence intervals for average speed in each lane
        avg_speeds_est = np.mean(avg_speeds_runs, axis=0)
        avg_speeds_high = np.percentile(avg_speeds_runs, q=97.5, axis=0)
        avg_speeds_low = np.percentile(avg_speeds_runs, q=2.5, axis=0)

        # remember average street speed
        intersection_avgs[intersection_factory.__name__] = np.mean(avg_speeds_runs)
        intersection_highs[intersection_factory.__name__] = np.percentile(avg_speeds_runs, q=97.5)
        intersection_lows[intersection_factory.__name__] = np.percentile(avg_speeds_runs, q=2.5)

        # data formatting
        err_high = avg_speeds_high - avg_speeds_est
        err_low = avg_speeds_est - avg_speeds_low

        # plot stuff
        ax.bar(
            x=list(range(avg_speeds_est.size)),
            width=0.8,
            height=avg_speeds_est,
            yerr=np.vstack([err_high, err_low])
        )

        ax.hlines(
            y=np.mean(avg_speeds_est),
            xmin=0,
            xmax=avg_speeds_est.size,
            linestyles="dashed",
            colors="orange",
        )

        ax.set_ylabel("average speed")
        ax.set_title(intersection_factory.__name__)
        ax.set_xticks([])

        mean_cmp_ax.plot(
            np.arange(avg_speeds_est.size),
            avg_speeds_est,
            marker="o",
            linestyle="dashed",
            label=intersection_factory.__name__
        )

        hist_cmp_ax.hist(
            avg_speeds_est,
            label=intersection_factory.__name__,
            alpha=0.2,
            histtype="stepfilled",
        )

    multifig.show()

    # scatterplot comparison
    mean_cmp_ax.vlines(
        np.arange(avg_speeds_est.size),
        ymin=0,
        ymax=5,
        linestyles="dashed",
        colors="black",
        alpha=0.2,
    )
    mean_cmp_ax.set_title("Average speeds on each street")
    mean_cmp_ax.set_ylabel("average speed")
    mean_cmp_ax.set_xticks([])
    mean_cmp_ax.legend()
    mean_cmp_fig.show()

    # histogram comparison
    hist_cmp_ax.set_title("Distribution of street average speeds")
    hist_cmp_ax.set_ylabel("# streets")
    hist_cmp_ax.set_xlabel("average speed")
    hist_cmp_ax.legend()
    hist_cmp_fig.show()

    # plot intersection comparison
    names = np.array(list(intersection_avgs.keys()))
    avgs = np.array(list(intersection_avgs.values()))
    highs = np.array(list(intersection_highs.values()))
    lows = np.array(list(intersection_lows.values()))

    # data formatting
    err_high = highs - avgs
    err_low = avgs - lows
    err = np.vstack([err_high, err_low])

    plt.figure(figsize=(10, 6))
    plt.bar(
        x=list(range(4)),
        width=0.8,
        height=avgs,
        tick_label=names,
        yerr=err,
    )
    plt.title("Average Street Speed")
    plt.show()


if __name__ == "__main__":
    make_plots()
