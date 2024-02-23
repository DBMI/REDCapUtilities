"""
Module test_string_cleanup.py, which performs automated
testing of the functions in string_cleanup.py
"""
import datetime
import pytest
from src.redcaputilities.string_cleanup import (
    clean_up_address,
    clean_up_date,
    clean_up_email,
    clean_up_phone,
    clean_up_string,
    clean_up_time,
)


def test_clean_up_address():
    #
    #   Convert 'P.O. Box' to 'PO Box'
    #
    address_proper: str = "PO Box 1234"
    address_raw: str = "P.O. box 1234"
    address_cleaned: str = clean_up_address(address_raw)
    assert isinstance(address_cleaned, str)
    assert address_cleaned == address_proper

    address_raw: str = "Po box 1234"
    address_cleaned: str = clean_up_address(address_raw)
    assert isinstance(address_cleaned, str)
    assert address_cleaned == address_proper

    # Ensure ordinary addresses aren't changed.
    address_raw = "123 Maple Street"
    address_cleaned = clean_up_address(address_raw)
    assert isinstance(address_cleaned, str)
    assert address_cleaned == address_raw
    #
    #   Extend 'St' to 'Street'
    #
    #   Test trailing punctuation.
    address_cleaned = clean_up_address("123 Maple St.")
    assert isinstance(address_cleaned, str)
    assert address_cleaned == "123 Maple Street"

    #   Test trailing whitespace.
    address_cleaned = clean_up_address("123 Maple Blvd ")
    assert isinstance(address_cleaned, str)
    assert address_cleaned == "123 Maple Boulevard"

    #   Tolerate "None" values.
    address_cleaned = clean_up_address(None)
    assert isinstance(address_cleaned, str)
    assert len(address_cleaned) == 0

    #   Ensure we're not expanding already-full names.
    address_cleaned = clean_up_address("123 Maple Street")
    assert isinstance(address_cleaned, str)
    assert address_cleaned == "123 Maple Street"

    #   Don't convert '4th' to '4Th', etc.
    address_cleaned = clean_up_address("123 4th St.")
    assert isinstance(address_cleaned, str)
    assert address_cleaned == "123 4th Street"


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

    #   Handle actual datetime object.
    date_string = "01/02/2023"
    datetime_obj = datetime.datetime.strptime(date_string, "%M/%d/%Y")
    date_string_cleaned = clean_up_date(input_string=datetime_obj)
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


def test_clean_up_email():
    #   Acceptable email passes right thru.
    assert len(clean_up_email(input_string="nobody@example.com")) > 0

    #   Nonsense emails are blanked.
    assert len(clean_up_email(input_string="NONE")) == 0
    assert len(clean_up_email(input_string="none")) == 0
    assert len(clean_up_email(input_string="None@ucsd.edu")) == 0
    assert len(clean_up_email(input_string="declined@example.com")) == 0
    assert len(clean_up_email(input_string="refuse@example.com")) == 0
    assert len(clean_up_email(input_string="refused@example.com")) == 0
    assert len(clean_up_email(input_string="unknown@nowhere.edu")) == 0

    #   Corner case.
    assert len(clean_up_email(input_string=None)) == 0

    #   Expect to raise an error:
    with pytest.raises(TypeError):
        clean_up_email(input_string=12345)


def test_clean_up_email_list():
    email_address_proper = "nobody@example.com"

    email_address_list = ["nobody@example.com", "nobody@example.com"]
    email_addresses_cleaned = clean_up_email(input_string=email_address_list)
    assert isinstance(email_addresses_cleaned, list)
    assert all(
        [
            phone_string == email_address_proper
            for phone_string in email_addresses_cleaned
        ]
    )


def test_clean_up_email_series(dataframe):
    email_address_proper = "nobody@example.com"
    dataframe["email"] = dataframe["email"].apply(clean_up_email)
    assert dataframe["email"][0] == email_address_proper

    email_address_cleaned = clean_up_email(dataframe["email"])
    assert email_address_cleaned == email_address_proper


def test_clean_up_phone():
    # Corner cases
    assert len(clean_up_phone(input_string="NONE")) == 0
    assert len(clean_up_phone(input_string="null")) == 0
    assert len(clean_up_phone(input_string="000-000-0000")) == 0
    assert len(clean_up_phone(input_string="619-000-0000")) == 0

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


def test_clean_up_strings(ignored_strings):
    #   Ensure 'normal' strings pass through unchanged.
    string = "123 Maple Street"
    string_cleaned = clean_up_string(
        input_string=string, strings_to_ignore=ignored_strings
    )
    assert isinstance(string_cleaned, str)
    assert string_cleaned == string

    #   Ensure 'ignored' strings are blanked.
    string = "345 Walnut Road"
    string_cleaned = clean_up_string(
        input_string=string, strings_to_ignore=ignored_strings
    )
    assert isinstance(string_cleaned, str)
    assert len(string_cleaned) == 0


def test_clean_up_strings_corner_cases(ignored_strings):
    string_cleaned = clean_up_string(
        input_string=1979, strings_to_ignore=ignored_strings
    )
    assert isinstance(string_cleaned, str)
    assert len(string_cleaned) == 0


def test_clean_up_string_list(ignored_strings):
    #   It's the second one that will be ignored.
    string_list = ["123 Maple Street", "234 Cherry Blvd.", "1600 Pennsylvania Ave."]
    strings_cleaned = clean_up_string(
        input_string=string_list, strings_to_ignore=ignored_strings
    )
    assert isinstance(strings_cleaned, list)
    assert len(strings_cleaned[0]) > 0
    assert len(strings_cleaned[1]) == 0
    assert len(strings_cleaned[2]) > 0


def test_clean_up_string_series(dataframe, ignored_strings):
    dataframe["address"] = dataframe["address"].apply(
        clean_up_string, strings_to_ignore=ignored_strings
    )
    assert len(dataframe["address"][0]) > 0


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
