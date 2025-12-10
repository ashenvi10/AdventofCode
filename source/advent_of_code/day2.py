from advent_of_code.utils import split_comma_separated_values


class InvalidIDParser:
    def __init__(self):
        self.invalid_ids: list[int] = []

    def parse_id_half_repeats(self, id: int) -> bool:

        if len(str(id)) % 2 != 0:
            return False

        first_half = str(id)[: len(str(id)) // 2]
        second_half = str(id)[len(str(id)) // 2 :]

        if first_half == second_half:
            self.invalid_ids.append(id)
            return True

        return False

    def parse_id_any_repeats(self, id: int) -> bool:

        length = len(str(id))

        # For up to half the length, check if any substring repeats
        for sub_length in range(1, length // 2 + 1):
            if length % sub_length != 0:
                continue
            substring = str(id)[:sub_length]
            repeats = length // sub_length
            if substring * repeats == str(id):
                self.invalid_ids.append(id)
                return True
        return False

    def get_invalid_ids(self, range_start: int, range_end: int, method: callable) -> list[int]:
        for id in range(range_start, range_end + 1):
            method(id)
        return self.invalid_ids

    def get_sum_of_invalid_ids(self, filepath: str, method: callable) -> int:

        range_values = split_comma_separated_values(filepath)
        ranges = [value.split("-") for value in range_values]
        ranges = [(int(start), int(end)) for start, end in ranges]

        for range_start, range_end in ranges:
            self.get_invalid_ids(range_start, range_end, method)

        return sum(self.invalid_ids)


if __name__ == "__main__":
    parser = InvalidIDParser()
    sum_of_ids = parser.get_sum_of_invalid_ids("inputs/day2.txt", parser.parse_id_any_repeats)
    print(f"Sum of invalid IDs: {sum_of_ids}")
