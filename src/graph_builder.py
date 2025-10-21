import networkx as nx
import numpy as np
from scipy.spatial import Delaunay

def build_graph(points):
    """
    Builds a graph based on Delaunay triangulation from a set of points.

    Args:
        points (np.ndarray): Coordinates of the points.

    Returns:
        nx.Graph: The constructed graph.
    """
    tri = Delaunay(points)
    G = nx.Graph()
    N = points.shape[0]
    G.add_nodes_from(range(N))

    for simplex in tri.simplices:
        G.add_edge(
            simplex[0],
            simplex[1],
            distance=np.linalg.norm(points[simplex[0]] - points[simplex[1]]),
        )
        G.add_edge(
            simplex[1],
            simplex[2],
            distance=np.linalg.norm(points[simplex[1]] - points[simplex[2]]),
        )
        G.add_edge(
            simplex[2],
            simplex[0],
            distance=np.linalg.norm(points[simplex[2]] - points[simplex[0]]),
        )
    return G
