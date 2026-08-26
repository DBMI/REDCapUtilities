"""
Module test_state_abbreviations.py,
    supports automated testing of FakeRecordGenerator class.

Classes
-------
TestSynthesizer
"""

import pandas
import pytest

from src.redcaputilities.state_abbr_conversion import StateAbbreviationConverter


def test_state_abbreviations():
    """Test conversion of 'CA' to 'California'."""
    state_abbreviation_converter = StateAbbreviationConverter()

    assert isinstance(state_abbreviation_converter, StateAbbreviationConverter)

    # One that should translate.
    abbr = "CA"
    full_state_name = state_abbreviation_converter.full_name(abbr)

    assert isinstance(full_state_name, str)
    assert full_state_name == "California"

    # One that should NOT.
    abbr = "XX"
    full_state_name = state_abbreviation_converter.full_name(abbr)

    assert isinstance(full_state_name, str)
    assert full_state_name == abbr


if __name__ == "__main__":  # pragma: no cover
    pass
