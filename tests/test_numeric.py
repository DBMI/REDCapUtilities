"""
Tests for the numeric utility functions.
"""

import pytest

from src.redcaputilities.numeric import is_even


def test_is_even():
    assert is_even(2)
    assert is_even(-2)
    assert not is_even(3)

    with pytest.raises(TypeError):
        is_even(1.5)
