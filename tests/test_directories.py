"""
    Tests for the directory utility functions.
"""
import os
import pytest
from src.redcaputilities.directories import ensure_output_path_exists


def test_ensure_path_exists():
    test_path = os.path.join(os.getcwd(), "test directory")

    if os.path.exists(test_path):
        os.rmdir(test_path)

    test_file = os.path.join(test_path, "test.txt")
    ensure_output_path_exists(test_file)
    assert os.path.exists(test_path)

    with pytest.raises(TypeError):
        ensure_output_path_exists(None)

    with pytest.raises(OSError):
        malformed_path = os.path.join(test_path, r"name that can't be? :/<parsed*?", 'nonsense.txt')
        ensure_output_path_exists(malformed_path)
