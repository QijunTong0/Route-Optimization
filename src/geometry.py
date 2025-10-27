import numpy as np


def angle_between_lines(common: np.ndarray, p1: np.ndarray, p2: np.ndarray) -> float:
    """
    2本の直線（それぞれ2点 p1-p2, p3-p4 で定義）がなす鋭角（小さい方）を
    度数で返します。

    Args:
        p1 (np.ndarray): 1本目の直線上の点1 (2次元)
        p2 (np.ndarray): 1本目の直線上の点2 (2次元)

    Returns:
        float: 2直線のなす鋭角（ラジアン単位、0からpi/2）
    """

    # 1. 各直線の方向ベクトルを計算
    v1 = p1 - common
    v2 = p2 - common

    # 2. 方向ベクトルを正規化（単位ベクトル化）
    # np.linalg.norm はベクトルのL2ノルム（大きさ）を計算します
    u1 = v1 / np.linalg.norm(v1)
    u2 = v2 / np.linalg.norm(v2)
    # 3. 単位ベクトルの内積（ドット積）を計算
    # u1・u2 = |u1||u2|cos(theta) = cos(theta)
    dot_product = np.clip(np.dot(u1, u2), -1.0, 1.0)

    # 4. 内積の絶対値を取り、arccosで角度を計算
    # abs(cos(theta)) を使うことで、角度を鋭角（0～pi/2）に限定します
    angle = np.arccos(np.abs(dot_product)) * 180 / np.pi
    if np.isnan(angle):
        angle = 0
    return angle
