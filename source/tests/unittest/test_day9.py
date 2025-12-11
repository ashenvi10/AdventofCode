from pathlib import Path

from advent_of_code.day9 import get_largest_red_green_rectangle, get_latest_rectangle_area, parse_input


def test_get_latest_rectangle_area(data_dir: Path):
    input = parse_input(data_dir / "day9.txt")
    assert get_latest_rectangle_area(input) == 50


def test_get_largest_red_green_rectangle(data_dir: Path):
    input = parse_input(data_dir / "day9.txt")
    assert get_largest_red_green_rectangle(input) == 24
