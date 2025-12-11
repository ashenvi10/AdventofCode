from pathlib import Path

import pytest


@pytest.fixture()
def data_dir() -> Path:
    """Returns the path to the data directory."""
    return Path(__file__).parents[1] / "test_inputs"
