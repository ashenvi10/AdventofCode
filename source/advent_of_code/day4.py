import numpy as np


class RollsCounter:
    def __init__(self):
        pass

    def count_rolls_in_square(self, rolls_square: np.ndarray) -> bool:

        centre_elem = rolls_square[1, 1]
        if centre_elem != "@":
            return False

        return (np.sum(rolls_square == "@") - 1) < 4

    def get_total_rolls_count(self, filepath: str, num_rounds: int | None = None) -> int:
        rolls_data = np.loadtxt(filepath, dtype=str, ndmin=2)

        # Split each element into individual characters
        rolls_data = np.array([[char for char in cell] for row in rolls_data for cell in row])

        # Pad the arrays with empty strings to handle edges
        padded_rolls = np.pad(rolls_data, pad_width=1, mode="constant", constant_values=".")

        # Get a 3x3 sliding window starting from 1,1 upto n-1,m-1
        total_rolls = 0

        rolls_to_remove_in_this_round = -1

        while rolls_to_remove_in_this_round != 0 and (num_rounds is None or num_rounds > 0):
            rolls_to_remove = []
            for i in range(1, padded_rolls.shape[0] - 1):
                for j in range(1, padded_rolls.shape[1] - 1):
                    rolls_square = padded_rolls[i - 1 : i + 2, j - 1 : j + 2]
                    if self.count_rolls_in_square(rolls_square):
                        rolls_to_remove.append((i, j))
                        total_rolls += 1

            for i, j in rolls_to_remove:
                padded_rolls[i, j] = "."
            rolls_to_remove_in_this_round = len(rolls_to_remove)
            if num_rounds is not None:
                num_rounds -= 1

        return total_rolls


if __name__ == "__main__":
    counter = RollsCounter()
    total_rolls = counter.get_total_rolls_count("inputs/day4.txt")
    print(f"Total rolls count: {total_rolls}")
