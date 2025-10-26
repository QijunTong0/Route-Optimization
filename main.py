from src.graph_builder import build_graph, expand_graph
from src.point_generator import generate_points
from src.visualizer import draw_graph_with_shortest_path

# 1. Generate points
num_random_points = 2
limit = 100
points, fixed_node_indices = generate_points(
    high=limit, num_random_points=num_random_points
)

# 2. Build graph
road = build_graph(points)

# 4. Visualize graph with shortest path
draw_graph_with_shortest_path(road, points, fixed_node_indices)
