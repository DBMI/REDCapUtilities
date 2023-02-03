"""
Contains test fixtures available across all test_*.py files.
"""
import pytest


@pytest.fixture(name="secure_data_directory")
def fixture_secure_data_directory() -> str:
    return r"F:\AoU_v2"
