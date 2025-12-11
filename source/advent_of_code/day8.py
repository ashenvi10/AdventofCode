import dataclasses
import itertools
from pathlib import Path

type Box = tuple[int, int, int]


def calculate_euclidean_distance(Box1: Box, Box2: Box) -> float:
    return sum((a - b) ** 2 for a, b in zip(Box1, Box2)) ** 0.5


@dataclasses.dataclass
class BoxCluster:
    boxes: list[Box]

    @property
    def size(self) -> int:
        return len(self.boxes)

    def __contains__(self, box: Box) -> bool:
        return box in self.boxes

    def __add__(self, other: "BoxCluster") -> "BoxCluster":
        return BoxCluster(self.boxes + other.boxes)


class BoxClusterer:

    def __init__(self, initial_boxes: list[Box]):
        self.initial_boxes = initial_boxes
        self.clusters: list[BoxCluster] = [BoxCluster([box]) for box in initial_boxes]

        self.distances = self.calculate_all_pairwise_distances()

    def calculate_all_pairwise_distances(self) -> dict[tuple[Box, Box], float]:
        distances = {}
        for box1, box2 in itertools.combinations(self.initial_boxes, 2):
            distances[(box1, box2)] = calculate_euclidean_distance(box1, box2)
        return distances

    def find_cluster_containing_box(self, box: Box) -> BoxCluster:
        for cluster in self.clusters:
            if box in cluster:
                return cluster
        raise ValueError(f"Box {box} not found in any cluster.")

    def cluster_boxes(self, *, max_iters: int | None = None) -> int | None:

        # Arrange the distances in ascending order
        sorted_distances = sorted(self.distances.items(), key=lambda item: item[1])

        iteration = 0

        for (box1, box2), distance in sorted_distances:
            iteration += 1
            if max_iters is not None and iteration >= max_iters:
                break

            cluster1 = self.find_cluster_containing_box(box1)
            cluster2 = self.find_cluster_containing_box(box2)

            if cluster1 is not cluster2:

                if max_iters is None and len(self.clusters) == 2:
                    return box1[0] * box2[0]

                # Merge clusters
                new_cluster = cluster1 + cluster2
                self.clusters.remove(cluster1)
                self.clusters.remove(cluster2)
                self.clusters.append(new_cluster)

            else:
                pass

    def get_part1_result(self) -> int:
        cluster_sizes = [cluster.size for cluster in self.clusters]
        sorted_sizes = sorted(cluster_sizes, reverse=True)
        return sorted_sizes[0] * sorted_sizes[1] * sorted_sizes[2]


def process_input_file(file_path: Path) -> list[Box]:
    boxes = []
    with file_path.open("r") as f:
        for line in f:
            x, y, z = map(int, line.strip().split(","))
            boxes.append((x, y, z))
    return boxes


if __name__ == "__main__":
    boxes = process_input_file(Path("inputs/day8.txt"))
    clusterer_part1 = BoxClusterer(boxes)
    clusterer_part1.cluster_boxes(max_iters=1000)
    print("Part 1 Result:", clusterer_part1.get_part1_result())

    clusterer_part2 = BoxClusterer(boxes)
    part2 = clusterer_part2.cluster_boxes()
    print("Part 2 Result:", part2)
