from advent_of_code.day1 import DialOrchestrator
from advent_of_code.utils import text_to_lines
from pathlib import Path


def test_count_end_value_occurrence(data_dir: Path):

    input_data = text_to_lines(data_dir / "day1.txt")
    orchestrator = DialOrchestrator(starting_value=50, max_value=99)

    occurrence_count = orchestrator.count_end_value_occurrence(input_data, target_value=0)
    assert occurrence_count == 3


def test_pass_through_zero(data_dir: Path):

    input_data = text_to_lines(data_dir / "day1.txt")
    orchestrator = DialOrchestrator(starting_value=50, max_value=99)

    pass_through_count = orchestrator.pass_through_zero(input_data)
    assert pass_through_count == 6
