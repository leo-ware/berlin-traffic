import matplotlib.pyplot as plt
import numpy as np


def plot_history(hist):
    step_numbers = []
    positions = []
    for step, arr in enumerate(hist):
        step_numbers.append([step]*len(arr))
        positions.append(arr)
    plt.scatter(np.hstack(positions), np.hstack(step_numbers), s=1, c="black")
    plt.ylabel("timestep")
    plt.xlabel("position")
    plt.show()
