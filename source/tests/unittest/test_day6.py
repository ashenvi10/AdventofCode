from pathlib import Path

import pytest
from advent_of_code.day6 import CephalopodMaths


class TestCephalopodMaths:

    def test_do_homework(self, data_dir: Path):
        maths = CephalopodMaths()
        result = maths.do_homework(data_dir / "day6.txt")
        assert result == 4277556

    def test_do_crazy_homework(self, data_dir: Path):
        maths = CephalopodMaths()
        result = maths.do_crazy_homework(data_dir / "day6.txt")
        assert result == 3263827
