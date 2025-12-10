from __future__ import annotations
import itertools
from pathlib import Path
import dataclasses
from functools import cached_property


@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

    def area(self, other: Point) -> int:
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


@dataclasses.dataclass(frozen=True)
class Line:
    start: Point
    end: Point

    def __contains__(self, point: Point) -> bool:
        return self.start.x <= point.x <= self.end.x and self.start.y <= point.y <= self.end.y


@dataclasses.dataclass(frozen=True)
class Rectangle:
    corner1: Point
    corner2: Point

    @property
    def corner3(self):
        return Point(x=self.corner1.x, y=self.corner2.y)

    @property
    def corner4(self):
        return Point(x=self.corner2.x, y=self.corner1.y)

    @property
    def all_corners(self) -> list[Point]:
        return [self.corner1, self.corner2, self.corner3, self.corner4]

    def get_perimeter(self) -> list[Line]:
        lines: list[Line] = []
        for corner1, corner2 in zip(self.all_corners, self.all_corners[1:] + [self.all_corners[0]]):
            start = corner1 if (corner1.x < corner2.x or corner1.y < corner2.y) else corner2
            end = corner2 if (corner1.x < corner2.x or corner1.y < corner2.y) else corner1
            lines.append(Line(start=start, end=end))
        return lines


@dataclasses.dataclass(frozen=True)
class Polygon:
    lines: list[Line]

    @cached_property
    def horizontal_lines(self) -> list[Line]:
        return [line for line in self.lines if line.start.y == line.end.y]

    @cached_property
    def vertical_lines(self) -> list[Line]:
        return [line for line in self.lines if line.start.x == line.end.x]

    def is_intersecting(self, line: Line) -> bool:
        if line.start.x == line.end.x:
            # Vertical line -- compare against horizontal lines
            for poly_line in self.horizontal_lines:
                if (
                    min(line.start.y, line.end.y) < poly_line.start.y < max(line.start.y, line.end.y)
                    and poly_line.start.x < line.start.x < poly_line.end.x
                ):
                    return True
        elif line.start.y == line.end.y:
            # Horizontal line -- compare against vertical lines
            for poly_line in self.vertical_lines:
                if (
                    poly_line.start.x > min(line.start.x, line.end.x)
                    and poly_line.start.x < max(line.start.x, line.end.x)
                    and poly_line.start.y < line.start.y < poly_line.end.y
                ):
                    return True
        return False

    def __contains__(self, point: Point) -> bool:
        # Include points on the perimeter and inside the polygon
        if any(point in line for line in self.lines):
            return True

        # A point is inside if there is a line on all four sides of it
        points_inside = (
            any(
                # Line to the left
                (line.start.x == line.end.x and line.start.x < point.x and line.start.y <= point.y <= line.end.y)
                for line in self.lines
            )
            and any(
                # Line to the right
                (line.start.x == line.end.x and line.start.x > point.x and line.start.y <= point.y <= line.end.y)
                for line in self.lines
            )
            and any(
                # Line below
                (line.start.y == line.end.y and line.start.y > point.y and line.start.x <= point.x <= line.end.x)
                for line in self.lines
            )
            and any(
                # Line above
                (line.start.y == line.end.y and line.start.y < point.y and line.start.x <= point.x <= line.end.x)
                for line in self.lines
            )
        )
        return points_inside


def get_latest_rectangle_area(points: list[Point]) -> int:

    point_combibnations = itertools.combinations(points, 2)
    areas = [point1.area(point2) for point1, point2 in point_combibnations]

    return max(areas)


def get_polygon(points: list[Point]) -> Polygon:
    lines = []
    for point1, point2 in zip(points, points[1:] + [points[0]]):
        if point1.x == point2.x:
            start = point1 if point1.y < point2.y else point2
            end = point2 if point1.y < point2.y else point1
            lines.append(Line(start=start, end=end))
        elif point1.y == point2.y:
            start = point1 if point1.x < point2.x else point2
            end = point2 if point1.x < point2.x else point1
            lines.append(Line(start=start, end=end))
        else:
            raise ValueError(f"Points {point1} and {point2} do not form a straight line.")
    return Polygon(lines=lines)


def get_largest_red_green_rectangle(points: list[Point]) -> int:

    point_combibnations = itertools.combinations(points, 2)
    areas = {Rectangle(point1, point2): point1.area(point2) for point1, point2 in point_combibnations}
    areas = sorted(areas.items(), key=lambda item: item[1])

    polygon = get_polygon(points)

    for rectangle, area in reversed(areas):
        perimeter_lines = rectangle.get_perimeter()
        if not any(polygon.is_intersecting(line) for line in perimeter_lines) and all(
            point in polygon for point in rectangle.all_corners
        ):
            return area


def parse_input(filepath: Path) -> list[Point]:
    points: list[Point] = []
    with filepath.open("r") as f:
        for line in f:
            x, y = map(int, line.strip().split(","))
            points.append(Point(x=x, y=y))
    return points


if __name__ == "__main__":
    input_path = Path("inputs/day9.txt")
    points = parse_input(input_path)
    area = get_latest_rectangle_area(points)
    print(f"Latest rectangle area: {area}")

    largest_area = get_largest_red_green_rectangle(points)
    print(f"Largest red-green rectangle area: {largest_area}")
