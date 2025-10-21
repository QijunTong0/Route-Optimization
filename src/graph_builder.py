import networkx as nx
import numpy as np
from scipy.spatial import Delaunay


def build_graph(points: np.ndarray):
    """
    Builds a graph based on Delaunay triangulation from a set of points.

    Args:
        points (np.ndarray): Coordinates of the points.

    Returns:
        nx.Graph: The constructed graph.
    """
    tri = Delaunay(points)
    road = nx.Graph()
    nums = points.shape[0]
    road.add_nodes_from(range(nums))

    for p in tri.simplices:
        road.add_edge(p[0], p[1], distance=np.linalg.norm(points[p[0]] - points[p[1]]))
        road.add_edge(p[1], p[2], distance=np.linalg.norm(points[p[1]] - points[p[2]]))
        road.add_edge(p[2], p[0], distance=np.linalg.norm(points[p[2]] - points[p[0]]))
    return road
