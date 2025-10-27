import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from src.graph_builder import expand_graph


def draw_graph_with_coordinates(graph: nx.Graph, label=False):
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
        with_labels=label,  # ノードIDを表示
        node_color="blue",  # ノードの色
        node_size=5,  # ノードのサイズ
        edge_color="gray",  # エッジの色
        font_size=5,
    )

    # 4. 座標プロットとして軸を正しく表示
    plt.axis("equal")  # X軸とY軸のスケールを合わせる (重要)

    plt.show()


def draw_graph_with_shortest_path(
    road: nx.Graph,
    source_node,
    target_node,
    limit=100,
    cost_ratio=0,
    suffix="",
):
    """
    Draws the graph and highlights the shortest path between two specified points.

    Args:
        G (nx.Graph): The NetworkX graph to draw.
        points (np.ndarray): Positions of the nodes.
        fixed_node_indices (list): Indices of the source_node and target_node [source_node, target_node].
        path_color (str): Color of the shortest path edges.
    """
    road = expand_graph(road, cost=cost_ratio)
    path_nodes = nx.shortest_path(
        road, source=source_node, target=target_node, weight="weight"
    )
    path_edges = list(zip(path_nodes[:-1], path_nodes[1:]))
    pos = nx.get_node_attributes(road, "coordinate")

    node_colors = ["blue"] * road.number_of_nodes()
    nx.draw_networkx_nodes(
        road,
        pos,
        node_size=10,
        node_color=node_colors,
    )
    nx.draw_networkx_edges(road, pos, width=0.5, edge_color="gray", alpha=0.7)
    nx.draw_networkx_edges(
        road, pos, edgelist=path_edges, width=2.5, edge_color="green", alpha=1.0
    )

    plt.xlim(-limit / 20, limit * 1.05)
    plt.ylim(-limit / 20, limit * 1.05)
    plt.gca().set_aspect("equal", adjustable="box")
    total_cost = 0
    turn_cost = 0
    distance_cost = 0
    for edge in path_edges:
        total_cost += road.edges[edge]["weight"]
        turn_cost += road.edges[edge]["turn_cost"]
        distance_cost += road.edges[edge]["distance"]
    plt.title(
        f"total_distance:{int(distance_cost)} m ; total_angle:{int(turn_cost*180)}°; cost_ratio:{round(cost_ratio,5)}"
    )
    plt.savefig(f"data/anime/out_{suffix:03d}.png")
    plt.close()


from src.graph_builder import expand_graph


def draw_graph_with_coordinates(graph: nx.Graph, label=False):
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
        with_labels=label,  # ノードIDを表示
        node_color="skyblue",  # ノードの色
        node_size=700,  # ノードのサイズ
        edge_color="gray",  # エッジの色
        font_size=20,
    )

    # 4. 座標プロットとして軸を正しく表示
    plt.axis("equal")  # X軸とY軸のスケールを合わせる (重要)

    plt.show()


def draw_graph(
    road: nx.Graph,
    source_node,
    target_node,
    limit=100,
    cost_ratio=0,
    suffix="",
):
    """
    Draws the graph and highlights the shortest path between two specified points.

    Args:
        G (nx.Graph): The NetworkX graph to draw.
        points (np.ndarray): Positions of the nodes.
        fixed_node_indices (list): Indices of the source_node and target_node [source_node, target_node].
        path_color (str): Color of the shortest path edges.
    """
    path_nodes = nx.shortest_path(
        road, source=source_node, target=target_node, weight="weight"
    )
    path_edges = list(zip(path_nodes[:-1], path_nodes[1:]))
    pos = nx.get_node_attributes(road, "coordinate")

    node_colors = ["blue"] * road.number_of_nodes()
    nx.draw_networkx_nodes(
        road,
        pos,
        node_size=10,
        node_color=node_colors,
    )
    nx.draw_networkx_edges(road, pos, width=0.5, edge_color="gray", alpha=0.7)
    nx.draw_networkx_edges(
        road, pos, edgelist=path_edges, width=2.5, edge_color="green", alpha=1.0
    )

    plt.xlim(-limit / 20, limit * 1.05)
    plt.ylim(-limit / 20, limit * 1.05)
    plt.gca().set_aspect("equal", adjustable="box")
    total_cost = 0
    turn_cost = 0
    distance_cost = 0
    for edge in path_edges:
        total_cost += road.edges[edge]["weight"]
        turn_cost += road.edges[edge]["turn_cost"]
        distance_cost += road.edges[edge]["distance"]
    plt.title(
        f"total_distance:{int(distance_cost)} m ; total_angle:{int(turn_cost)}°; cost_ratio:{round(cost_ratio,5)}"
    )
    plt.savefig(f"data/anime/out_{suffix:03d}.png")
    plt.close()
