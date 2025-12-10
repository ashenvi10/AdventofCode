from pathlib import Path
from typing import NamedTuple
from advent_of_code.utils import text_to_lines


class FreshIngredientSorter:
    def __init__(self, inventory: list[tuple[int, int]]):
        self.inventory = inventory

    def sort_inventory(self, inventory: list[tuple[int, int]]) -> list[tuple[int, int]]:
        return sorted(inventory)

    def sort_fresh_ingredients(self, ingredients: list[int]) -> int:

        total_fresh = 0
        for ingredient in ingredients:
            for item in self.inventory:
                if item[0] <= ingredient <= item[1]:
                    total_fresh += 1
                    break
        return total_fresh

    def is_overlap(self, range1: tuple[int, int], range2: tuple[int, int]) -> bool:
        return (range1[0] <= range2[1]) and (range1[1] >= range2[0])

    def get_combined_inventory_item(self, ranges: list[tuple[int, int]]) -> tuple[int, int]:

        new_low = min([r[0] for r in ranges])
        new_high = max([r[1] for r in ranges])
        return (new_low, new_high)

    def get_all_fresh_ingredients_from_inventory(self) -> int:

        total_fresh = 0

        old_items = self.sort_inventory(self.inventory)
        new_items = self.run_check_loop(old_items)

        for item in new_items:
            total_fresh += item[1] - item[0] + 1

        return total_fresh

    def run_check_loop(self, old_items: list[tuple[int, int]]) -> list[tuple[int, int]]:

        new_items = old_items + [-1]

        while new_items != old_items:

            try:
                new_items.remove(-1)
            except ValueError:
                pass

            old_items = new_items

            items_in_any_completed_chain = []
            current_chain = []
            new_items = []

            for item1 in old_items:

                if item1 in items_in_any_completed_chain:
                    continue

                current_chain.append(item1)

                for item2 in old_items:

                    if item1 == item2:
                        continue
                    if item2 in items_in_any_completed_chain:
                        continue

                    if self.is_overlap(item1, item2):
                        current_chain.append(item2)

                items_in_any_completed_chain.extend(current_chain)
                combined_item = self.get_combined_inventory_item(current_chain)
                new_items.append(combined_item)
                current_chain = []

        return new_items


class InventoryAndIngredients(NamedTuple):
    inventory: list[tuple[int, int]]
    ingredients: list[int]


def get_inventory_and_ingredients(filepath: Path) -> InventoryAndIngredients:
    inventory = []
    ingredients = []
    pantry = text_to_lines(filepath)

    separator_index = pantry.index("")
    for line in pantry[:separator_index]:
        low, high = map(int, line.split("-"))
        inventory.append((low, high))
    for line in pantry[separator_index + 1 :]:
        ingredients.append(int(line))

    return InventoryAndIngredients(inventory=inventory, ingredients=ingredients)


if __name__ == "__main__":

    pantry = get_inventory_and_ingredients(Path("inputs/day5.txt"))
    sorter = FreshIngredientSorter(inventory=pantry.inventory)
    fresh_count = sorter.sort_fresh_ingredients(pantry.ingredients)
    print(f"Number of fresh ingredients: {fresh_count}")

    total_fresh = sorter.get_all_fresh_ingredients_from_inventory()
    print(f"Total fresh ingredients from inventory: {total_fresh}")
