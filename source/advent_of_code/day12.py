from pathlib import Path
import numpy as np
import dataclasses
from typing import NamedTuple
@dataclasses.dataclass(frozen=True)
class Present:
    id: int 
    shape: np.ndarray

    def area(self) -> int:
        return int(np.sum(self.shape))

@dataclasses.dataclass
class Tree:
    space: int
    presents_count: list[int]

    def area_required_for_presents(self, presents: list[Present]) -> int:
        total_area = 0
        for count, present in zip(self.presents_count, presents):
            total_area += count * present.area()
        return total_area
    
    def is_valid(self, presents: list[Present]) -> bool:
        return self.area_required_for_presents(presents) <= self.space
    
class PresentCollection(NamedTuple):
    presents: list[Present]
    trees: list[Tree]

    

def parse_input(filepath: Path) -> PresentCollection:
    with open(filepath, "r") as file:
        lines = file.readlines()

    # The line breaks define the separation between presents
    line_breaks = [i for i, line in enumerate(lines) if line.strip() == ""]

    presents = []
    # Iterate up to the penultimate line break because the last one is not a present
    for start, end in zip([0] + [idx + 1 for idx in line_breaks], line_breaks):
        present_id = int(lines[start].split(":")[0].strip())
        shape_lines = lines[start+1:end] 
        shape_array = np.array([[1 if char == '#' else 0 for char in line.strip()] for line in shape_lines])
        presents.append(Present(id=present_id, shape=shape_array))

    trees = []
    for line in lines[line_breaks[-1]+1:]:
        space_dimension = line.split(":")[0]
        space = int(space_dimension.split("x")[0]) * int(space_dimension.split("x")[1])
        presents_count = line.split(":")[1].split(" ")
        presents_count = [int(count.strip()) for count in presents_count if count.strip() != '']
        trees.append(Tree(space=space, presents_count=presents_count))

    return PresentCollection(presents=presents, trees=trees)

def calculate_valid_trees(present_collection: PresentCollection) -> int:
    valid_trees = 0
    for tree in present_collection.trees:
        if tree.is_valid(present_collection.presents):
            valid_trees += 1
    return valid_trees
        
            

if __name__ == "__main__":
    present_collection = parse_input(Path("inputs/day12.txt"))
    valid_trees_count = calculate_valid_trees(present_collection)
    print(f"Number of valid trees: {valid_trees_count}")


