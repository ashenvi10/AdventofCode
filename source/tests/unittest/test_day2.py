from pathlib import Path

from advent_of_code.day2 import InvalidIDParser


def test_get_sum_of_invalid_ids(data_dir: Path):

    parser = InvalidIDParser()
    sum_of_ids = parser.get_sum_of_invalid_ids(data_dir / "day2.txt", parser.parse_id_half_repeats)
    assert sum_of_ids == 1227775554


def test_get_sum_of_more_invalid_ids(data_dir: Path):

    parser = InvalidIDParser()
    sum_of_ids = parser.get_sum_of_invalid_ids(data_dir / "day2.txt", parser.parse_id_any_repeats)
    assert sum_of_ids == 4174379265
