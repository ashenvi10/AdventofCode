import numpy as np
from advent_of_code.utils import text_to_lines

ACTIONS = {
    "+": np.sum,
    "*": np.prod,
}


class CephalopodMaths:
    def do_homework(self, filepath: str) -> int:
        homework_problem = np.loadtxt(filepath, dtype=str, ndmin=2)

        actions = homework_problem[-1, :]
        homework_numbers = np.array([[int(cell) for cell in row] for row in homework_problem[:-1, :]])

        result = 0
        for col in range(homework_numbers.shape[1]):

            numbers = homework_numbers[:, col]
            action = actions[col]
            if action in ACTIONS:
                result += ACTIONS[action](numbers)

        return result

    def do_crazy_homework(self, filepath: str) -> int:
        homework_problem = text_to_lines(filepath)

        actions = homework_problem[-1].split()
        homework_numbers = np.array([list(line) for line in homework_problem[:-1]])

        # Find the indices which separate the number columns. This is where all entries are spaces.
        breaking_cols = [i for i, col in enumerate(homework_numbers.T) if all(col == " ")]
        breaking_cols.insert(0, -1)
        breaking_cols.insert(len(breaking_cols), homework_numbers.shape[1])

        result = 0
        for idx, col in enumerate(breaking_cols):
            if idx == 0:
                continue  # Skip the first breaking column
            string_numbers = homework_numbers[:, breaking_cols[idx - 1] + 1 : col]

            # Transpose and flatten each number column to get the actual numbers
            numbers = [int("".join(row)) for row in string_numbers.T]

            action = actions[idx - 1]
            if action in ACTIONS:
                result += ACTIONS[action](numbers)

        return result


if __name__ == "__main__":
    maths = CephalopodMaths()
    normal_result = maths.do_homework("inputs/day6.txt")
    print(f"Cephalopod Maths Homework Result: {normal_result}")

    crazy_result = maths.do_crazy_homework("inputs/day6.txt")
    print(f"Cephalopod Crazy Maths Homework Result: {crazy_result}")
