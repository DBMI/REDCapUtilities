"""
Module test_string_cleanup.py, which performs automated
testing of the functions in string_cleanup.py
"""
import pytest
from src.redcaputilities.string_cleanup import (
    clean_up_date,
    clean_up_phone,
    clean_up_time,
    extend_street_abbreviations,
)


def test_clean_up_date():
    date_string_proper = "2023-01-02"

    date_string = "01/02/2023"
    date_string_cleaned = clean_up_date(input_string=date_string)
    assert isinstance(date_string_cleaned, str)
    assert date_string_cleaned == date_string_proper

    date_string = "1/2/2023"
    date_string_cleaned = clean_up_date(input_string=date_string)
    assert isinstance(date_string_cleaned, str)
    assert date_string_cleaned == date_string_proper

    date_string = "January 2, 2023"
    date_string_cleaned = clean_up_date(input_string=date_string)
    assert isinstance(date_string_cleaned, str)
    assert date_string_cleaned == date_string_proper

    date_string_cleaned = clean_up_date(input_string=date_string_proper)
    assert isinstance(date_string_cleaned, str)
    assert date_string_cleaned == date_string_proper

    # Expect to raise an error:
    with pytest.raises(TypeError):
        clean_up_date(input_string=12345)

    # Test if it can't parse.
    date_string_cleaned = clean_up_date(input_string="ABCDEFG")
    assert isinstance(date_string_cleaned, str)
    assert len(date_string_cleaned) == 0

    date_string_cleaned = clean_up_date(input_string=None)
    assert isinstance(date_string_cleaned, str)
    assert len(date_string_cleaned) == 0


def test_clean_up_date_list():
    date_string_proper = "2023-01-02"

    date_string_list = ["01/02/2023", "1/2/2023", "January 2, 2023"]
    date_strings_cleaned = clean_up_date(input_string=date_string_list)
    assert isinstance(date_strings_cleaned, list)
    assert all(
        [date_string == date_string_proper for date_string in date_strings_cleaned]
    )


def test_clean_up_date_series(dataframe):
    date_string_proper = "2023-01-02"
    dataframe["dob"] = dataframe["dob"].apply(clean_up_date)
    assert dataframe["dob"][0] == date_string_proper

    date_string_cleaned = clean_up_date(dataframe["dob"])
    assert date_string_cleaned == date_string_proper


def test_clean_up_phone():
    # Corner cases
    assert len(clean_up_phone(input_string="NONE")) == 0
    assert len(clean_up_phone(input_string="null")) == 0
    assert len(clean_up_phone(input_string="0000000000")) == 0
    assert clean_up_phone(input_string="SA6-1706") == "SA6-1706"

    phone_string_proper = "123-456-7890"
    phone_cleaned = clean_up_phone(input_string="123-456-7890")
    assert isinstance(phone_cleaned, str)
    assert phone_cleaned == phone_string_proper

    phone_cleaned = clean_up_phone(input_string="1-123-456-7890")
    assert isinstance(phone_cleaned, str)
    assert phone_cleaned == phone_string_proper

    phone_cleaned = clean_up_phone(input_string="1234567890")
    assert isinstance(phone_cleaned, str)
    assert phone_cleaned == phone_string_proper

    # Expect to raise an error:
    with pytest.raises(TypeError):
        clean_up_phone(input_string=12345)

    phone_string_cleaned = clean_up_phone(input_string=None)
    assert isinstance(phone_string_cleaned, str)
    assert len(phone_string_cleaned) == 0


def test_clean_up_phone_list():
    phone_string_proper = "123-456-7890"

    phone_strings_list = ["123-456-7890", "1-123-456-7890", "1234567890"]
    phone_strings_cleaned = clean_up_phone(input_string=phone_strings_list)
    assert isinstance(phone_strings_cleaned, list)
    assert all(
        [phone_string == phone_string_proper for phone_string in phone_strings_cleaned]
    )


def test_clean_up_phone_series(dataframe):
    phone_string_proper = "123-456-7890"
    dataframe["phone"] = dataframe["phone"].apply(clean_up_phone)
    assert dataframe["phone"][0] == phone_string_proper

    phone_string_cleaned = clean_up_phone(dataframe["phone"])
    assert phone_string_cleaned == phone_string_proper


def test_clean_up_time():
    time_string_proper = "15:01:02"

    time_string = "01/02/2023 3:01:02 PM"
    time_string_cleaned = clean_up_time(input_string=time_string)
    assert isinstance(time_string_cleaned, str)
    assert time_string_cleaned == time_string_proper

    time_string = "1/2/2023 15:01:02"
    time_string_cleaned = clean_up_time(input_string=time_string)
    assert isinstance(time_string_cleaned, str)
    assert time_string_cleaned == time_string_proper

    time_string = "January 2, 2023 3:01:02 PM"
    time_string_cleaned = clean_up_time(input_string=time_string)
    assert isinstance(time_string_cleaned, str)
    assert time_string_cleaned == time_string_proper

    time_string_cleaned = clean_up_time(input_string=time_string_proper)
    assert isinstance(time_string_cleaned, str)
    assert time_string_cleaned == time_string_proper

    # Test if it can't parse.
    time_string_cleaned = clean_up_time(input_string="ABCDEFG")
    assert isinstance(time_string_cleaned, str)
    assert len(time_string_cleaned) == 0

    # Expect to raise an error:
    with pytest.raises(TypeError):
        clean_up_time(input_string=12345)

    time_string_cleaned = clean_up_time(input_string=None)
    assert isinstance(time_string_cleaned, str)
    assert len(time_string_cleaned) == 0


def test_clean_up_time_list():
    time_string_proper = "15:01:02"

    time_strings_list = [
        "01/02/2023 3:01:02 PM",
        "1/2/2023 15:01:02",
        "January 2, 2023 3:01:02 PM",
    ]
    time_strings_cleaned = clean_up_time(input_string=time_strings_list)
    assert isinstance(time_strings_cleaned, list)
    assert all(
        [time_string == time_string_proper for time_string in time_strings_cleaned]
    )


def test_clean_up_time_series(dataframe):
    time_string_proper = "15:01:02"
    dataframe["time"] = dataframe["time"].apply(clean_up_time)
    assert dataframe["time"][0] == time_string_proper

    time_string_cleaned = clean_up_time(dataframe["time"])
    assert time_string_cleaned == time_string_proper


def test_extend_abbreviations():
    #   Test trailing punctuation.
    address_cleaned = extend_street_abbreviations("123 Maple St.")
    assert isinstance(address_cleaned, str)
    assert address_cleaned == "123 Maple Street"

    #   Test trailing whitespace.
    address_cleaned = extend_street_abbreviations("123 Maple Blvd ")
    assert isinstance(address_cleaned, str)
    assert address_cleaned == "123 Maple Boulevard"

    #   Tolerate "None" values.
    address_cleaned = extend_street_abbreviations(None)
    assert address_cleaned is None

    #   Ensure we're not expanding already-full names.
    address_cleaned = extend_street_abbreviations("123 Maple Street")
    assert isinstance(address_cleaned, str)
    assert address_cleaned == "123 Maple Street"

    #   Don't convert '4th' to '4Th', etc.
    address_cleaned = extend_street_abbreviations("123 4th St.")
    assert isinstance(address_cleaned, str)
    assert address_cleaned == "123 4th Street"
