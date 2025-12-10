from advent_of_code.day4 import RollsCounter
from pathlib import Path
import pytest


@pytest.mark.parametrize(
    "num_rounds, expected_count",
    [
        (1, 13),
        (None, 43),
    ],
)
def test_get_sum_of_more_invalid_ids(data_dir: Path, num_rounds: int | None, expected_count: int):

    roll_counter = RollsCounter()
    sum_of_ids = roll_counter.get_total_rolls_count(data_dir / "day4.txt", num_rounds=num_rounds)
    assert sum_of_ids == expected_count
