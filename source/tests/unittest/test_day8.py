from pathlib import Path

from advent_of_code.day8 import BoxClusterer, process_input_file


def test_part1(data_dir: Path):

    boxes = process_input_file(data_dir / "day8.txt")
    clusterer = BoxClusterer(boxes)
    clusterer.cluster_boxes(max_iters=11)

    assert clusterer.get_part1_result() == 40


def test_part2(data_dir: Path):

    boxes = process_input_file(data_dir / "day8.txt")
    clusterer = BoxClusterer(boxes)
    part2 = clusterer.cluster_boxes()

    assert part2 == 25272
