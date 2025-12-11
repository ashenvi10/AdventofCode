from pathlib import Path
from typing import NamedTuple

from advent_of_code.utils import text_to_lines

direction_map = {
    "L": -1,
    "R": 1,
}


class TurnResult(NamedTuple):
    start_value: int
    passes_through_zero: int


class DialOrchestrator:
    def __init__(self, *, starting_value: int, max_value: int = 99):
        self._current_value = starting_value
        self.max_value = max_value

    @property
    def current_value(self) -> int:
        """Get the current value."""
        return self._current_value

    @current_value.setter
    def current_value(self, value: int) -> None:
        """Set the current value."""
        self._current_value = value

    def turn(self, move: str) -> TurnResult:
        """Apply the move to the current value."""

        direction_char = move[0]
        distance = int(move[1:])

        passes_through_zero: int = 0

        # Add or subtract the distance based on direction - L is subtract, R is add
        shifted_value = self.current_value + direction_map[direction_char] * distance

        if shifted_value == 0:
            passes_through_zero = 1
        elif shifted_value > self.max_value:
            passes_through_zero = shifted_value // (self.max_value + 1)
        elif shifted_value < 0:
            if self.current_value == 0:
                passes_through_zero = abs(shifted_value) // (self.max_value + 1)
            else:
                passes_through_zero = 1 + (abs(shifted_value) // (self.max_value + 1))

        self.current_value = shifted_value % (self.max_value + 1)

        return TurnResult(start_value=self.current_value, passes_through_zero=passes_through_zero)

    def count_end_value_occurrence(self, moves: list[str], target_value: int) -> int:
        """Count how many times the target value is reached during the moves."""

        count = 0

        for move in moves:
            self.turn(move)
            if self.current_value == target_value:
                count += 1

        return count

    def pass_through_zero(self, moves: list[str]) -> bool:
        """Check if the target value is passed through during the moves."""

        passes_through_zero = 0

        for move in moves:
            result = self.turn(move)
            passes_through_zero += result.passes_through_zero

        return passes_through_zero


if __name__ == "__main__":
    orchestrator_part1 = DialOrchestrator(starting_value=50, max_value=99)
    input_data = text_to_lines(Path("inputs/day1.txt"))
    occurrence_count = orchestrator_part1.count_end_value_occurrence(input_data, target_value=0)
    print(occurrence_count)

    orchestrator_part2 = DialOrchestrator(starting_value=50, max_value=99)
    pass_through_count = orchestrator_part2.pass_through_zero(input_data)
    print(pass_through_count)
