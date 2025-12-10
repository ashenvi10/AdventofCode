from pathlib import Path
from advent_of_code.utils import text_to_lines
import functools


class RaySplitter:

    @property
    def all_splitter_positions(self) -> list:
        return self._all_splitter_positions

    @all_splitter_positions.setter
    def all_splitter_positions(self, value: list) -> None:
        self._all_splitter_positions = value

    def spread_beam(self, filepath: Path) -> int:

        data = text_to_lines(filepath)
        data = [list(line) for line in data]
        # Exclude any rows that do not contain 'S' or '^'
        data = [line for idx, line in enumerate(data) if ("S" in line or "^" in line) or idx == len(data) - 1]

        splitters_hit = 0
        starting_position = {idx for idx, val in enumerate(data[0]) if val == "S"}

        beam_positions = [starting_position]
        all_splitter_positions = [[]]

        for idx, line in enumerate(data[1:]):
            splitter_positions = [idx for idx, val in enumerate(line) if val == "^"]
            all_splitter_positions.append(splitter_positions)

            new_beam_positions = set()

            for pos in beam_positions[idx]:
                if pos in splitter_positions:
                    splitters_hit += 1
                    if pos > 0:
                        new_beam_positions.add(pos - 1)
                    if pos < len(line) - 1:
                        new_beam_positions.add(pos + 1)
                else:
                    new_beam_positions.add(pos)

            beam_positions.append(new_beam_positions)

        self.all_splitter_positions = all_splitter_positions

        return splitters_hit, starting_position.pop()

    def count_root_to_leaf_paths(self, filepath: Path) -> int:

        _, starting_position = self.spread_beam(filepath)

        # For each position in the last row, count the number of unique paths leading to it
        total_paths = self.paths_from_position(starting_position, 0)

        return total_paths

    @functools.cache
    def paths_from_position(self, position: int, row_idx: int) -> int:
        if row_idx == len(self.all_splitter_positions) - 1:
            return 1

        if position in self.all_splitter_positions[row_idx]:
            return self.paths_from_position(position - 1, row_idx) + self.paths_from_position(position + 1, row_idx)
        else:
            return self.paths_from_position(position, row_idx + 1)


if __name__ == "__main__":
    ray_splitter = RaySplitter()
    result = ray_splitter.spread_beam(Path("inputs/day7.txt"))
    print(f"Number of splitters hit by the beam: {result[0]}")

    total_paths = ray_splitter.count_root_to_leaf_paths(Path("inputs/day7.txt"))
    print(f"Total unique root-to-leaf paths: {total_paths}")
