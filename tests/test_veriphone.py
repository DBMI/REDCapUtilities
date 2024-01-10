"""
Module test_veriphone.py, which performs automated
testing of the Veriphone class in veriphone.py
"""
import pandas
from src.redcaputilities.veriphone import Veriphone


def test_veriphone_instantiation(multiple_dataframe):
    obj = Veriphone()
    assert isinstance(obj, Veriphone)

    # UCSD number ought to work.
    # assert obj.validate_one_phone_number("858-534-2230")

    # Ought to return invalid due to character "O" instead of zero.
    # assert not obj.validate_one_phone_number("858-534-223O")

    # Try a list of two numbers, one valid, one not.
    numbers: list = ["858-534-2230", "858-534-223O"]
    numbers_cleaned: list = obj.validate_phone_numbers(numbers)
    assert isinstance(numbers_cleaned, list)
    assert len(numbers_cleaned) == 2
    assert numbers_cleaned[0] == "858-534-2230"
    assert numbers_cleaned[1] == ""

    # pandas.Series
    numbers_cleaned: pandas.Series = obj.validate_phone_numbers(multiple_dataframe['phone'])
    assert isinstance(numbers_cleaned, pandas.Series)
    assert len(numbers_cleaned) == 2
    assert numbers_cleaned[0] == "858-534-2230"
    assert numbers_cleaned[1] == ""
