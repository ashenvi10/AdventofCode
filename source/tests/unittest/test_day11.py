from pathlib import Path

from advent_of_code.day11 import ServerRack, parse_input


def test_calculate_total_paths(data_dir: Path):
    server_outputs = parse_input(data_dir / "day11_part1.txt")
    server_rack = ServerRack(server_outputs)
    total_paths = server_rack.calculate_total_paths(start_server="you", end_server="out")
    assert total_paths == 5


def test_calculate_total_paths_with_includes(data_dir: Path):
    server_outputs = parse_input(data_dir / "day11_part2.txt")
    server_rack = ServerRack(server_outputs)
    total_paths = server_rack.calculate_paths_through(
        start_server="svr", end_server="out", through_servers=("dac", "fft")
    )
    assert total_paths == 2
