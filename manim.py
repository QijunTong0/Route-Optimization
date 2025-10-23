from manim.animation.creation import Create
from manim.animation.fading import FadeIn, FadeOut
from manim.animation.movement import MoveAlongPath
from manim.constants import DOWN
from manim.mobject.geometry.arc import Dot
from manim.mobject.geometry.line import Line
from manim.mobject.text.text_mobject import Text
from manim.mobject.types.vectorized_mobject import VMobject, VGroup
from manim.scene.scene import Scene
from manim.utils.rate_functions import linear
from manim.utils.color import RED, YELLOW, GRAY, WHITE
import numpy as np

# --- Configuration ---
# Set the speed of the moving dot (in Manim units per second)
DOT_SPEED = 2.0
# ---------------------


class PathFollowing(Scene):
    """
    A Manim scene that draws a graph and animates a point
    moving along a specified path at a constant speed.
    """

    def construct(self):
        # 1. --- Define Your Graph Data ---
        # (x, y, z) coordinates for each vertex. z is 0 for 2D.
        vertex_coords = {
            "v1": np.array([-3, -1, 0]),
            "v2": np.array([3, -1, 0]),
            "v3": np.array([-3, 2, 0]),
            "v4": np.array([3, 2, 0]),
            "v5": np.array([0, 3, 0]),
        }

        # Edges defined by pairs of vertex keys
        edges = [
            ("v1", "v2"),
            ("v1", "v3"),
            ("v2", "v4"),
            ("v3", "v4"),
            ("v3", "v5"),
            ("v4", "v5"),
        ]

        # Path defined by an ordered list of vertex keys
        path_to_follow = ["v1", "v3", "v5", "v4", "v2"]
        # ------------------------------------

        # 2. Create and draw the full graph
        graph_mob = self.create_graph_mobject(vertex_coords, edges)

        self.play(Create(graph_mob), run_time=2)
        self.wait(0.5)

        # 3. Create and draw the highlighted path
        path_mob = self.create_path_mobject(vertex_coords, path_to_follow)

        self.play(Create(path_mob), run_time=1)
        self.wait(0.5)

        # 4. Create the moving dot
        start_point = vertex_coords[path_to_follow[0]]
        moving_dot = Dot(point=start_point, color=RED, radius=0.12)

        self.play(FadeIn(moving_dot))

        # 5. Animate the dot moving along the path
        # Get the total length of the path
        path_length = path_mob.get_arc_length()

        # Calculate the total time needed based on speed
        total_run_time = path_length / DOT_SPEED

        # Animate the dot moving along the path Mobject
        # 'rate_func=linear' ensures the speed is constant
        self.play(
            MoveAlongPath(moving_dot, path_mob),
            run_time=total_run_time,
            rate_func=linear,
        )

        # 6. Clean up
        self.play(FadeOut(moving_dot), FadeOut(path_mob))
        self.wait(1)

    def create_graph_mobject(self, coords, edges):
        """Helper function to create the graph Mobject."""

        # Create dots and labels for vertices
        vertices_mob = VGroup()
        for key, coord in coords.items():
            dot = Dot(point=coord, color=WHITE)
            label = Text(key, font_size=20).next_to(dot, DOWN, buff=0.15)
            vertices_mob.add(VGroup(dot, label))  # Group dot and label

        # Create lines for edges
        edges_mob = VGroup()
        for v1_key, v2_key in edges:
            if v1_key in coords and v2_key in coords:
                start_p = coords[v1_key]
                end_p = coords[v2_key]
                edge_line = Line(start_p, end_p, color=GRAY, stroke_width=3)
                edges_mob.add(edge_line)

        # Group all parts of the graph
        graph_mob = VGroup(edges_mob, vertices_mob)
        return graph_mob

    def create_path_mobject(self, coords, path_keys):
        """Helper function to create the path VMobject."""

        # Get the sequence of coordinates for the path
        path_points = [coords[key] for key in path_keys if key in coords]

        # Create a VMobject (vectorized mobject) from the points
        path_line = VMobject(color=YELLOW, stroke_width=6)
        path_line.set_points_as_corners(path_points)

        return path_line
