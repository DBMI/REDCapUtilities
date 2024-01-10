"""
Contains test fixtures available across all test_*.py files.
"""
import pandas
import pytest


@pytest.fixture(name="dataframe")
def fixture_dataframe() -> pandas.DataFrame:
    df = pandas.DataFrame(
        {
            "name": "Alice",
            "address": "123 Maple Street",
            "dob": "01/02/2023",
            "email": "nobody@example.com",
            "phone": "1-123-456-7890",
            "time": "3:01:02 PM",
        },
        index=[0],
    )
    return df


@pytest.fixture(name="ignored_strings")
def fixture_ignored_strings() -> list:
    return ["234 Cherry Blvd.", "345 Walnut Road"]


@pytest.fixture(name="multiple_dataframe")
def fixture_multiple_dataframe() -> pandas.DataFrame:
    df1 = pandas.DataFrame(
        {
            "name": "Alice",
            "phone": "858-534-2230",
        },
        index=[0],
    )
    df2 = pandas.DataFrame(
        {
            "name": "Bob",
            "phone": "858-534-223O",
        },
        index=[1],
    )
    return pandas.concat([df1, df2])


@pytest.fixture(name="secure_data_directory")
def fixture_secure_data_directory() -> str:
    return r"F:\dbmi.data\redcap_refresh"
