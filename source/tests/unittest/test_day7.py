from pathlib import Path
from advent_of_code.day7 import RaySplitter


def test_spread_beam(data_dir: Path):
    ray_splitter = RaySplitter()
    result = ray_splitter.spread_beam(data_dir / "day7.txt")
    assert result[0] == 21


def test_count_root_to_leaf_paths(data_dir: Path):
    ray_splitter = RaySplitter()
    result = ray_splitter.count_root_to_leaf_paths(data_dir / "day7.txt")
    assert result == 40
