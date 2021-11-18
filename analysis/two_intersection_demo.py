from src.network import build_network
from src.dataviz import space_time_plot
import matplotlib.pyplot as plt
import networkx as nx


def main():
    # network = build_network(nodes, edges, entry_points, exit_points)
    network = build_network(list("AB"), [["A", "B", 5]])

    lane0 = network.lanes[0]
    lane1 = network.lanes[1]

    # draw the network
    nx.draw(network.graph, network.pos())
    nx.draw_networkx_labels(network.graph, network.pos())
    plt.show()

    # push fake car data
    lane0.push([1, 5, 6, 8])

    # store history of each lane
    hist1 = []
    hist2 = []

    # run the model
    for _ in range(40):
        network.step()
        hist1.append(network.lanes[0].to_array())
        hist2.append(network.lanes[1].to_array())

    space_time_plot(hist1, show=False, label="a -> b", c="blue")
    space_time_plot(hist2, show=False, label="b -> a", c="red")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
