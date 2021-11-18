
from src.graphs.berlin_map import *
# from src.graphs.simple import *

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def make_graph(edges):
    """generate graph from edge data"""
    G = nx.Graph()
    for id, (u, v, length) in enumerate(edges):
        G.add_edge(u, v, id=id, length=length)
    return G


def get_layout(G):
    """layout used for all plotting"""
    return nx.kamada_kawai_layout(G, weight="length")


def draw_map(G, pos):
    """draws the map without any fanciness"""
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos=pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos=pos)
    plt.show()


def get_adj_matrix(G):
    """calculate the transition matrix for the model"""
    adj = np.zeros((len(G.edges), len(G.edges)))

    for u, v, i in G.edges.data("id"):
        for node in [u, v]:
            for edge in G[node].values():
                adj[i, edge["id"]] += 1
    adj = np.where(adj, 1, 0)

    # remove self-connections
    # adj = adj - np.identity(adj.shape[0])

    adj = adj / np.sum(adj, axis=1)

    return adj


def adjust_for_length(G, adj, max_r_i = 0.5):
    """calculate the length-adjusted transition matrix"""
    i = np.identity(adj.shape[0])

    lengths = np.array([l for (*_, l) in G.edges.data("length")])
    # scale lengths such that the largest take `longest_road` steps to traverse
    relative_lengths = max_r_i*lengths/np.max(lengths)

    # augment the diagonal
    adj = np.where(adj > 0, 1, 0)
    adj = ((adj / np.sum(adj, axis=0)) * (1 - relative_lengths)) + (i * relative_lengths)

    return adj


def get_steady_states(adj):
    eigvecs = np.linalg.eig(adj)[1]

    # we only want eigenvectors which can be interpreted as likelihoods
    # this means only eigenvectors whose elements all have the same sign
    pos_eigvecs = eigvecs[:, np.all(eigvecs >= 0, axis=0) | np.all(eigvecs <= 0, axis=0)]

    # normalize to get steady state distributions (and kill negatives)
    pos_eigvecs /= np.sum(pos_eigvecs, axis=0)

    # columns are steady states
    return pos_eigvecs


def plot_edge_heatmap(G, pos, densities, ax):
    """Plots a heatmap of edge density for a given steady state A"""
    return nx.draw(
        G,
        pos=pos,
        with_labels=True,
        edge_color=densities,
        edge_vmin=0,
        edge_vmax=np.max(densities),
        edge_cmap=plt.get_cmap("Reds"),
        ax=ax
    )


def plot_density_barchart(G, densities, ax, sort=False):
    names = [f"{u} <-> {v}" for u, v in G.edges]

    # optionally sort by height (pretty)
    if sort:
        zipped = list(zip(names, densities))
        zipped.sort(key=lambda item: item[1], reverse=True)
        names = [item[0] for item in zipped]
        densities = [item[1] for item in zipped]

    x_pos = np.linspace(0, 1, len(densities))
    ax.bar(x_pos, densities, tick_label=names, width=0.8 / densities.size)
    ax.set_ylabel("relative density")

    # thank you stack exchange
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)


def draw_graph_from_densities(G, densities):
    """takes a graph and makes the cool visualization you see"""
    pos = get_layout(G)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 10))
    plot_edge_heatmap(G, pos, densities, ax1)
    plot_density_barchart(G, densities, ax2)

    return fig


G = make_graph(edges)
adj = get_adj_matrix(G)

# plot without length adjustment
steady_states = get_steady_states(adj)
densities = steady_states[:, 0]

# plot with length adjustment
lengths = np.array([l for (*_, l) in G.edges.data("length")])
adj_adjusted = adjust_for_length(G, adj)
adjusted_steady_states = get_steady_states(adj_adjusted)
adjusted_densities = adjusted_steady_states[:, 0]
adjusted_densities /= lengths


def draw_graphs():
    unadjusted_fig = draw_graph_from_densities(G, densities)
    unadjusted_fig.suptitle("Density of Streets (unadjusted model)")
    unadjusted_fig.show()

    adjusted_fig = draw_graph_from_densities(G, adjusted_densities)
    adjusted_fig.suptitle("Density of Streets (length-adjusted model)")
    adjusted_fig.show()


if __name__ == "__main__":
    draw_graphs()
