import numpy as np


def generate_points(high=100, num_random_points=50):
    """
    Generates fixed and random points.

    Args:
        num_random_points (int): The number of random points to generate.

    Returns:
        np.ndarray: Coordinates of all points.
        list: Indices of the fixed points.
    """
    random_points = np.random.randint(1, high, size=(num_random_points, 2))
    fixed_points = np.array(
        [
            [0, 0],
            [high, high],
            [high, 0],
            [0, high],
        ]
    )
    points = np.vstack([fixed_points, random_points])
    fixed_node_indices = list(range(len(fixed_points)))
    return points, fixed_node_indices
