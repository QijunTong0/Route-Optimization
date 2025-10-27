import numpy as np

from src.graph_builder import build_graph, expand_graph
from src.point_generator import generate_points
from src.visualizer import draw_graph_with_coordinates

np.random.seed(1234)
# 1. Generate points
num_random_points = 4
limit = 100
points, fixed_node_indices = generate_points(
    high=limit, num_random_points=num_random_points
)

# 2. Build graph
road = build_graph(points)
road_exp = expand_graph(road, cost=0, interp=0.2)
draw_graph_with_coordinates(road_exp, label=True)
