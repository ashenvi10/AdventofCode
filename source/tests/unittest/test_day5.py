from pathlib import Path

import pytest
from advent_of_code.day5 import FreshIngredientSorter, get_inventory_and_ingredients


def test_fresh_ingredients(data_dir: Path):
    pantry = get_inventory_and_ingredients(data_dir / "day5.txt")
    sorter = FreshIngredientSorter(inventory=pantry.inventory)
    fresh_count = sorter.sort_fresh_ingredients(pantry.ingredients)
    assert fresh_count == 3


@pytest.mark.parametrize(
    "range1, range2, expected",
    [
        ((1, 5), (4, 8), True),
        ((4, 8), (1, 5), True),
        ((1, 3), (4, 6), False),
        ((4, 6), (1, 3), False),
        ((5, 10), (10, 15), True),
        ((10, 15), (5, 10), True),
    ],
)
def test_is_overlap(data_dir: Path, range1: tuple[int, int], range2: tuple[int, int], expected: bool):
    pantry = get_inventory_and_ingredients(data_dir / "day5.txt")
    sorter = FreshIngredientSorter(inventory=pantry.inventory)
    assert sorter.is_overlap(range1, range2) == expected


@pytest.mark.parametrize(
    "range1, range2, expected",
    [
        ((1, 5), (4, 8), (1, 8)),
        ((10, 15), (12, 20), (10, 20)),
    ],
)
def test_get_combined_inventory_item(
    data_dir: Path, range1: tuple[int, int], range2: tuple[int, int], expected: tuple[int, int]
):
    pantry = get_inventory_and_ingredients(data_dir / "day5.txt")
    sorter = FreshIngredientSorter(inventory=pantry.inventory)
    assert sorter.get_combined_inventory_item([range1, range2]) == expected


def test_get_all_fresh_ingredients_from_inventory(data_dir: Path):
    pantry = get_inventory_and_ingredients(data_dir / "day5.txt")
    sorter = FreshIngredientSorter(inventory=pantry.inventory)
    total_fresh = sorter.get_all_fresh_ingredients_from_inventory()
    assert total_fresh == 14
