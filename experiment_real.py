import networkx as nx
import numpy as np
import osmnx as ox

from src.visualizer import draw_graph_with_shortest_path

# NetworkX のグラフとして取得

top = 35.67960
bottom = 35.656607
left = 139.47887
right = 139.539762
G = ox.graph_from_bbox((left, bottom, right, top), network_type="bike")

# --- これで G は networkx の MultiDiGraph です ---


print(f"ノード数: {len(G.nodes)}")
print(f"エッジ数: {len(G.edges)}")

df_nodes, df_edges = ox.graph_to_gdfs(G)

road = nx.Graph()
for node, attr in G.nodes(data=True):
    road.add_node(node, coordinate=np.array([attr["x"], attr["y"]]))

for e1, e2, _ in G.edges:
    attr = df_edges.loc[(e1, e2, _)]
    is_koushu = 10**5 if attr["name"] == "甲州街道" else 1.0
    road.add_edge(e1, e2, weight=attr.length * is_koushu)

source_node = 1636628761
target_node = 196957475

draw_graph_with_shortest_path(
    road,
    source_node=source_node,
    target_node=target_node,
    interp=0.0,
    suffix=0,
    cost_ratio=0,
)
