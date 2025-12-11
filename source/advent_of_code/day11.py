import functools
from itertools import permutations
from pathlib import Path

from advent_of_code.utils import text_to_lines


def parse_input(filepath: Path) -> dict[str, list[str]]:
    lines = text_to_lines(filepath)
    server_outputs = {line.split(":")[0]: line.split(":")[1].strip().split() for line in lines}
    return server_outputs


class ServerRack:
    def __init__(self, server_outputs: dict[str, list[str]]):
        self.server_outputs = server_outputs

    @functools.cache
    def calculate_total_paths(self, *, start_server: str, end_server: str) -> int:
        """Calculates the total number of distinct paths from start_server to end_server and gets all such paths."""
        if start_server == end_server:
            return 1

        total_paths = 0
        for next_server in self.server_outputs.get(start_server, []):
            total_paths += self.calculate_total_paths(start_server=next_server, end_server=end_server)

        return total_paths

    def calculate_paths_through(self, *, start_server: str, end_server: str, through_servers: tuple[str, ...]) -> int:

        # Paths from start -> end via another server = paths from start to that server * paths from that server to end
        total_paths = 0

        # Generate all permutations of the through_servers to consider all possible orders
        through_server_permutations = permutations(through_servers)
        server_setpoints = [
            [start_server] + list(permuted_servers) + [end_server] for permuted_servers in through_server_permutations
        ]

        for server_setpoint in server_setpoints:
            path_count = 1
            for i in range(len(server_setpoint) - 1):
                path_count *= self.calculate_total_paths(
                    start_server=server_setpoint[i], end_server=server_setpoint[i + 1]
                )
            total_paths += path_count

        return total_paths


if __name__ == "__main__":
    server_outputs = parse_input(Path("inputs/day11.txt"))
    server_rack = ServerRack(server_outputs)
    total_paths = server_rack.calculate_total_paths(start_server="you", end_server="out")
    print(f"Total distinct paths from 'you' to 'out': {total_paths}")

    total_paths_with_includes = server_rack.calculate_paths_through(
        start_server="svr", end_server="out", through_servers=("dac", "fft")
    )
    print(f"Total distinct paths from 'svr' to 'out' through 'dac' and 'fft': {total_paths_with_includes}")
