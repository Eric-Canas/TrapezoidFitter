from __future__ import annotations
import numpy as np


class _Line:
    """
    Class to represent a line in 2D space defined by two points (x1, y1) and (x2, y2).
    The line equation is represented in the form Ax + By + C = 0.
    """

    def __init__(self, x1: float | int, y1: float | int, x2: float | int, y2: float | int):
        """
        Initialize a _Line instance with two points (x1, y1) and (x2, y2).

        :param x1: float | int. x-coordinate of the first point.
        :param y1: float | int. y-coordinate of the first point.
        :param x2: float | int. x-coordinate of the second point.
        :param y2: float | int. y-coordinate of the second point.
        """
        self.A, self.B, self.C = self.calculate_line_coefficients(x1=x1, y1=y1, x2=x2, y2=y2)

    def calculate_line_coefficients(self, x1: float | int, y1: float | int, x2: float | int, y2: float | int) -> tuple[
        float, float, float]:
        """
        Calculate the coefficients A, B, and C of the line equation Ax + By + C = 0.

        :param x1: float | int. x-coordinate of the first point.
        :param y1: float | int. y-coordinate of the first point.
        :param x2: float | int. x-coordinate of the second point.
        :param y2: float | int. y-coordinate of the second point.
        :return: tuple[float, float, float]. Tuple containing the coefficients A, B, and C.
        """
        # Equation derived from two-point form
        A, B, C = y2 - y1, x1 - x2, x2 * y1 - x1 * y2
        return A, B, C

    def move_line(self, distance: float | int):
        """
        Move the line in the direction perpendicular to it by a specified distance.

        :param distance: float | int. Distance by which to move the line.
        """
        # Delta C is derived by translating the line equation Ax + By + C = 0
        delta_C = -distance * np.sqrt(self.A ** 2 + self.B ** 2)
        self.C += delta_C

    def move_line_to_intersect_point(self, x: float | int, y: float | int) -> tuple[float, float]:
        """
        Move the line to intersect a given point (x, y).

        :param x: float | int. The x-coordinate of the point.
        :param y: float | int. The y-coordinate of the point.
        :return: tuple[float, float]. New A, B, C coefficients of the line.
        """
        # Calculate the new C such that the line goes through the point (x, y)
        self.C = -(self.A * x + self.B * y)
        return self.A, self.B, self.C

    def distance_from_point(self, x: float | int, y: float | int) -> float:
        """
        Calculate the distance of a point (x, y) from the line.

        :param x: float | int. The x-coordinate of the point.
        :param y: float | int. The y-coordinate of the point.
        :return: float. Distance of the point from the line.
        """
        return abs(self.point_line_position(x=x, y=y)) / np.sqrt(self.A ** 2 + self.B ** 2)

    def point_line_position(self, x: float | int, y: float | int) -> float:
        """
        Calculate the position of a point (x, y) relative to the line.
        The value will be positive, negative, or zero depending on the point's position.

        :param x: float | int. The x-coordinate of the point.
        :param y: float | int. The y-coordinate of the point.
        :return: float. Position value.
        """
        return self.A * x + self.B * y + self.C

    def get_intersection(self, other_line: _Line) -> tuple[float, float] | None:
        """
        Find the intersection point between this line and another line.

        :param other_line: _Line. The other line represented as an instance of the _Line class.
        :return: tuple[float, float] | None. Tuple representing the intersection point, or None if lines are parallel.
        """
        # Using Cramer's method to solve the system of equations formed by the two lines
        # A1*x + B1*y + C1 = 0 and A2*x + B2*y + C2 = 0
        det = self.A * other_line.B - other_line.A * self.B

        if det == 0:
            # Lines are parallel, no intersection
            return None

        x = (-self.C * other_line.B + other_line.C * self.B) / det
        y = (-self.A * other_line.C + other_line.A * self.C) / det

        return x, y
