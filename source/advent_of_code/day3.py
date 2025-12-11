from pathlib import Path

from advent_of_code.utils import text_to_lines


class JoltageCalculator:
    def __init__(self):
        pass

    def get_largest_jolt_in_bank(self, bank: str, num_batts: int) -> int:

        bank_split = [int(bk_str) for bk_str in bank]

        num_batts_left = num_batts
        max_jolts = []
        max_jolt_id = -1

        while num_batts_left > 0:
            bank_split = bank_split[max_jolt_id + 1 :]

            if num_batts_left == 1:
                current_max = max(bank_split)
            else:
                current_max = max(bank_split[: -(num_batts_left - 1)])
            max_jolts.append(str(current_max))
            max_jolt_id = [idx for idx, elem in enumerate(bank_split) if elem == current_max][0]
            num_batts_left -= 1

        return int("".join(max_jolts))

    def get_total_maximum_joltage(self, filepath: Path, num_batts: int):
        input_data = text_to_lines(filepath)

        max_joltages = 0
        for input in input_data:
            max_joltages += self.get_largest_jolt_in_bank(input, num_batts)

        return max_joltages


if __name__ == "__main__":
    calculator = JoltageCalculator()
    max_joltage = calculator.get_total_maximum_joltage(Path("inputs/day3.txt"), 12)
    print(max_joltage)
