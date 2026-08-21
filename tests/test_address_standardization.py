"""
Module test_address_standardization.py, which performs automated
testing of the AddressStandardizer class.
"""
from src.redcaputilities.address_standardizer import AddressStandardizer


def test_address_standardization():
    addr_stndzer = AddressStandardizer()
    assert isinstance(addr_stndzer, AddressStandardizer)

    address_raw = "123 2nd Avenue #234"
    address_standardized = addr_stndzer.standardize_street_address(address_raw)
    assert isinstance(address_standardized, str)
    assert address_standardized == "123 2ND AVE APT 234"

    address_raw = "123 2nd Avenue Apt 234"
    address_standardized = addr_stndzer.standardize_street_address(address_raw)
    assert isinstance(address_standardized, str)
    assert address_standardized == "123 2ND AVE APT 234"

    address_raw = "123 West Maple Street"
    address_standardized = addr_stndzer.standardize_street_address(address_raw)
    assert isinstance(address_standardized, str)
    assert address_standardized == "123 W MAPLE ST"

    address_raw = "123 W. Maple Street"
    address_standardized = addr_stndzer.standardize_street_address(address_raw)
    assert isinstance(address_standardized, str)
    assert address_standardized == "123 W MAPLE ST"

    address_raw = "123 Apple Boulevard"
    address_standardized = addr_stndzer.standardize_street_address(address_raw)
    assert isinstance(address_standardized, str)
    assert address_standardized == "123 APPLE BLVD"

    address_raw = "123Apple Boulevard"
    address_standardized = addr_stndzer.standardize_street_address(address_raw)
    assert isinstance(address_standardized, str)
    assert address_standardized == "123 APPLE BLVD"

    address_raw = "12N Lakeside Drive"
    address_standardized = addr_stndzer.standardize_street_address(address_raw)
    assert isinstance(address_standardized, str)
    assert address_standardized == "12N LAKESIDE DR"

    address_raw = "P.O. Box 1234"
    address_standardized = addr_stndzer.standardize_street_address(address_raw)
    assert isinstance(address_standardized, str)
    assert address_standardized == "PO BOX 1234"

    address_raw = "P O Box 1234"
    address_standardized = addr_stndzer.standardize_street_address(address_raw)
    assert isinstance(address_standardized, str)
    assert address_standardized == "PO BOX 1234"


def test_address_standardization_list():
    addr_stndzer = AddressStandardizer()
    assert isinstance(addr_stndzer, AddressStandardizer)
    address_proper = "123 W MAPLE ST"

    address_list = ["123 West Maple Street", "123 W MAPLE ST"]
    addresses_cleaned = addr_stndzer.standardize_street_address(address=address_list)
    assert isinstance(addresses_cleaned, list)
    assert all([address == address_proper for address in addresses_cleaned])


if __name__ == "__main__":
    pass
