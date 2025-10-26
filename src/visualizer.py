import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def draw_graph_with_coordinates(graph: nx.Graph):
    """
    NetworkXグラフの 'coordinate' 属性（Numpy配列）に基づいて
    ノードを空間的に配置して描画する関数。

    Args:
        G (nx.Graph): 'coordinate' 属性を持つノードを含むグラフ。
    """

    # 1. 'coordinate' 属性から位置情報を辞書として取得
    #    形式: {node_id: np.array([x, y]), ...}
    pos = nx.get_node_attributes(graph, "coordinate")

    # 2. 属性が存在するかチェック
    if not pos:
        raise ValueError

    # 3. グラフの描画
    plt.figure(figsize=(8, 8))  # 描画サイズを指定

    nx.draw_networkx(
        graph,
        pos=pos,  # ここで取得した座標辞書を指定
        with_labels=False,  # ノードIDを表示
        node_color="blue",  # ノードの色
        node_size=80,  # ノードのサイズ
        edge_color="gray",  # エッジの色
        font_size=10,
    )

    # 4. 座標プロットとして軸を正しく表示
    plt.axis("equal")  # X軸とY軸のスケールを合わせる (重要)

    plt.show()


def draw_graph_with_shortest_path(
    road: nx.Graph,
    points: np.ndarray,
    fixed_node_indices,
    path_color="green",
    limit=100,
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
        road, pos, edgelist=path_edges, width=2.5, edge_color=path_color, alpha=1.0
    )

    plt.xlim(-limit / 20, limit * 1.05)
    plt.ylim(-limit / 20, limit * 1.05)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.savefig("./data/minimum_path.svg")
