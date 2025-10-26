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
        road.add_edge(p[0], p[1], distance=np.linalg.norm(points[p[0]] - points[p[1]]))
        road.add_edge(p[1], p[2], distance=np.linalg.norm(points[p[1]] - points[p[2]]))
        road.add_edge(p[2], p[0], distance=np.linalg.norm(points[p[2]] - points[p[0]]))
    return road


def expand_graph(road: nx.Graph, st_ind=0, ed_ind=1, cost=1, interp=0.05):
    road_epd = nx.Graph()
    road_epd.add_node("s", coordinate=np.array([0, 0]))
    road_epd.add_node("t", coordinate=np.array([1, 1]))
    for node in road.nodes:
        for e1, e2 in combinations(road.edges([node]), 2):
            node1 = f"{node}_{e1[1]}"
            node2 = f"{node}_{e2[1]}"
            road_epd.add_node(
                node1,
                coordinate=(1 - interp) * road.nodes[node]["coordinate"]
                + interp * road.nodes[e1[1]]["coordinate"],
            )
            road_epd.add_node(
                node2,
                coordinate=(1 - interp) * road.nodes[node]["coordinate"]
                + interp * road.nodes[e2[1]]["coordinate"],
            )
            angle_cost = cost * angle_between_lines(
                road.nodes[node]["coordinate"],
                road.nodes[e1[1]]["coordinate"],
                road.nodes[e2[1]]["coordinate"],
            )
            road_epd.add_edge(node1, node2, weight=angle_cost)
            if node == st_ind:
                road_epd.add_edge("s", node1, weight=0)
                road_epd.add_edge("s", node2, weight=0)
            if node == ed_ind:
                road_epd.add_edge("t", node1, weight=0)
                road_epd.add_edge("t", node2, weight=0)

    for e1, e2, attr in road.edges(data=True):
        road_epd.add_edge(f"{e1}_{e2}", f"{e2}_{e1}", weight=attr["distance"])
    return road_epd
