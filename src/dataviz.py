import matplotlib.pyplot as plt
import numpy as np


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
