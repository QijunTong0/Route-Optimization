import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def draw_graph(G, points, fixed_node_indices):
    """
    Draws the graph.

    Args:
        G (nx.Graph): The NetworkX graph to draw.
        points (np.ndarray): Coordinates of the nodes.
        fixed_node_indices (list): Indices of the fixed points.
    """
    plt.figure(figsize=(8, 8))
    pos = {i: points[i] for i in range(points.shape[0])}
    node_colors = ["blue"] * points.shape[0]
    for idx in fixed_node_indices:
        node_colors[idx] = "red"

    nx.draw(
        G,
        pos,
        with_labels=False,
        node_size=70,
        node_color=node_colors,
        width=0.5,
        edge_color="gray",
    )
    plt.gca().set_aspect("equal", adjustable="box")
    plt.show()


def draw_graph_with_shortest_path(
    road: nx.Graph, points: np.ndarray, fixed_node_indices, path_color="green"
):
    """
    Draws the graph and highlights the shortest path between two specified points.

    Args:
        G (nx.Graph): The NetworkX graph to draw.
        points (np.ndarray): Positions of the nodes.
        fixed_node_indices (list): Indices of the source_node and target_node [source_node, target_node].
        path_color (str): Color of the shortest path edges.
    """
    source_node = fixed_node_indices[0]
    target_node = fixed_node_indices[1]

    path_nodes = nx.shortest_path(
        road, source=source_node, target=target_node, weight="distance"
    )
    path_edges = list(zip(path_nodes[:-1], path_nodes[1:]))

    plt.figure(figsize=(8, 8))
    pos = {i: points[i] for i in range(points.shape[0])}
    node_colors = ["blue"] * road.number_of_nodes()
    for idx in fixed_node_indices:
        node_colors[idx] = "red"

    nx.draw_networkx_nodes(road, pos, node_size=70, node_color=node_colors)
    nx.draw_networkx_edges(road, pos, width=0.5, edge_color="gray", alpha=0.7)
    nx.draw_networkx_edges(
        road,
        pos,
        edgelist=path_edges,
        width=2.5,
        edge_color=path_color,
        alpha=1.0,
    )

    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.savefig("./data/minimum_path.svg")
