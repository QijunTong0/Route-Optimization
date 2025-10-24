from itertools import combinations

import networkx as nx
import numpy as np
from scipy.spatial import Delaunay

from src.geometry import angle_between_lines


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
    for i, point in enumerate(points):
        road.add_node(i, coordinate=point)

    for p in tri.simplices:
        road.add_edge(
            int(p[0]), int(p[1]), distance=np.linalg.norm(points[p[0]] - points[p[1]])
        )
        road.add_edge(
            int(p[1]), int(p[2]), distance=np.linalg.norm(points[p[1]] - points[p[2]])
        )
        road.add_edge(
            int(p[2]), int(p[0]), distance=np.linalg.norm(points[p[2]] - points[p[0]])
        )
    return road


def exapnd_graph(road: nx.Graph):
    road_epd = nx.Graph()
    for id, attr in road.nodes(data=True):
        for e1, e2 in combinations(road.edges([id]), 2):
            node1 = f"{id}_{e1[1]}"
            node2 = f"{id}_{e2[1]}"
            road_epd.add_node(node1)
            road_epd.add_node(node2)
            angle_cost = angle_between_lines(1, 1, 1)
            road_epd.add_edge(node1, node2, angle_cost)
