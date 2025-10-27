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
        road.add_edge(p[0], p[1], weight=np.linalg.norm(points[p[0]] - points[p[1]]))
        road.add_edge(p[1], p[2], weight=np.linalg.norm(points[p[1]] - points[p[2]]))
        road.add_edge(p[2], p[0], weight=np.linalg.norm(points[p[2]] - points[p[0]]))
    return road


def expand_graph(road: nx.Graph, st_ind=0, ed_ind=1, cost=1, interp=0.05):
    road_epd = nx.Graph()
    for node in road.nodes:
        if road.degree[node] == 1:
            e1 = list(road.edges([node]))[0]
            node1 = f"{node}_{e1[1]}"
            road_epd.add_node(
                node1,
                coordinate=(1 - interp) * road.nodes[node]["coordinate"]
                + interp * road.nodes[e1[1]]["coordinate"],
            )

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
            angle = angle_between_lines(
                road.nodes[node]["coordinate"],
                road.nodes[e1[1]]["coordinate"],
                road.nodes[e2[1]]["coordinate"],
            )
            road_epd.add_edge(
                node1, node2, weight=cost * angle, turn_cost=angle, distance=0
            )
    road_epd.add_node("s", coordinate=road.nodes[st_ind]["coordinate"])
    road_epd.add_node("t", coordinate=road.nodes[ed_ind]["coordinate"])
    for node in road_epd.nodes:
        if node.split("_")[0] == str(st_ind):
            road_epd.add_edge("s", node, weight=0, turn_cost=0, distance=0)
        if node.split("_")[0] == str(ed_ind):
            road_epd.add_edge("t", node, weight=0, turn_cost=0, distance=0)

    for e1, e2, attr in road.edges(data=True):
        road_epd.add_edge(
            f"{e1}_{e2}",
            f"{e2}_{e1}",
            weight=attr["weight"],
            turn_cost=0,
            distance=attr["weight"],
        )
    return road_epd
