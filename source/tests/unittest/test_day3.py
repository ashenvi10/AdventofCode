from pathlib import Path

import pytest
from advent_of_code.day3 import JoltageCalculator


@pytest.mark.parametrize(
    "num_batts, expected_joltage",
    [
        (2, 357),
        (12, 3121910778619),
    ],
)
def test_get_total_maximum_joltage(data_dir: Path, num_batts: int, expected_joltage: int):
    calculator = JoltageCalculator()

    occurrence_count = calculator.get_total_maximum_joltage(data_dir / "day3.txt", num_batts)
    assert occurrence_count == expected_joltage
