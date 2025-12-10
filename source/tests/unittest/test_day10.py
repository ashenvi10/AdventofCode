from pathlib import Path
from advent_of_code.day10 import main
import pytest

@pytest.mark.parametrize("for_lighting, for_joltage, expected", [
    (True, False, 7), # part 1
    (False, True, 33), # part 2
])
def test_main(data_dir: Path, for_lighting: bool, for_joltage: bool, expected: int):
    filepath = data_dir / "day10.txt"
    result = main(filepath, for_lighting=for_lighting, for_joltage=for_joltage)
    assert result == expected
