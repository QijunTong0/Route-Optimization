import numpy as np


def angle_between_lines(
    common: np.ndarray, p_st: np.ndarray, p_ed: np.ndarray
) -> float:
    """
    2本の直線（それぞれ2点 p1-p2, p3-p4 で定義）がなす鋭角（小さい方）を
    ラジアン単位で返します。

    Args:
        p1 (np.ndarray): 1本目の直線上の点1 (2次元)
        p2 (np.ndarray): 1本目の直線上の点2 (2次元)

    Returns:
        float: 2直線のなす鋭角（ラジアン単位、0からpi/2）
    """

    # 1. 各直線の方向ベクトルを計算
    v1 = common - p_st
    v2 = p_ed - common

    # 2. 方向ベクトルを正規化（単位ベクトル化）
    # np.linalg.norm はベクトルのL2ノルム（大きさ）を計算します
    u1 = v1 / np.linalg.norm(v1)
    u2 = v2 / np.linalg.norm(v2)

    # 3. 単位ベクトルの内積（ドット積）を計算
    # u1・u2 = |u1||u2|cos(theta) = cos(theta)
    dot_product = np.clip(np.dot(u1, u2), -1.0, 1.0)

    angle = np.arccos(dot_product) / np.pi

    return angle
