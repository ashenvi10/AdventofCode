from pathlib import Path


def read_file(filepath: Path) -> str:
    """Reads the content of a file and returns it as a string."""

    with open(filepath, "r") as f:
        return f.read()


def text_to_lines(filepath: Path) -> list[str]:
    """Splits the input text into a list of lines."""
    content = read_file(filepath)
    return content.strip().splitlines()


def split_comma_separated_values(filepath: Path) -> list[str]:
    """Splits a comma-separated string into a list of values."""
    line = read_file(filepath)
    return [value.strip() for value in line.split(",")]
