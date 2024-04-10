import collections
import usaddress
import os.path
from importlib import resources  # type: ignore[import]
import pandas  # type: ignore[import]
import string
from typing import Union


class AddressStandardizer:
    """
    Standardizes US addresses according to US Postal Service rules.
        (see https://pe.usps.com/text/pub28/welcome.htm)
    """

    def __init__(self):
        # Get abbreviation list to turn "North" into "N".
        self.__direction_abbrev_dict: dict = self.__build_direction_abbreviations_dict()

        # Get abbreviation list to turn "Glen" into "GLN".
        self.__street_abbrev_dict: dict = self.__build_street_abbreviations_dict()

        # Get abbreviation list to turn "Apartment" into "APT".
        self.__unit_abbrev_dict: dict = self.__build_unit_abbreviations_dict()

    def __abbreviate_direction(self, direction: str) -> str:
        """Abbreviates 'Northeast' to 'NE', according to USPS rules.

        Parameters
        ----------
        direction : str

        Returns
        -------
        dir : str
        """
        if not isinstance(direction, str):
            raise TypeError("Input 'direction' is not the expected string.")

        # Remove whitespace, punctuation & convert to uppercase.
        direction = self.__clean_text(direction)

        try:
            direct: str = self.__direction_abbrev_dict[direction]
        except KeyError:
            direct = direction

        return direct

    def __abbreviate_street_type(self, street_type: str) -> str:
        """Abbreviates 'Street' to 'St', 'Avenue' to 'Ave', according to USPS rules.

        Parameters
        ----------
        street_type : str

        Returns
        -------
        st_typ : str
        """
        if not isinstance(street_type, str):
            raise TypeError("Input 'street_type' is not the expected string.")

        # Remove whitespace, punctuation & convert to uppercase.
        street_type = self.__clean_text(street_type)

        try:
            st_typ: str = self.__street_abbrev_dict[street_type]
        except KeyError:
            st_typ = street_type

        return st_typ

    def __abbreviate_unit_type(self, occupancy_type: str) -> str:
        """Abbreviates 'Apartment' to 'APT', according to USPS rules.

        Parameters
        ----------
        occupancy_type : str

        Returns
        -------
        occ_type : str
        """
        if not isinstance(occupancy_type, str):
            raise TypeError("Input 'occupancy_type' is not the expected string.")

        # Remove whitespace, punctuation & convert to uppercase.
        occupancy_type = self.__clean_text(occupancy_type)

        try:
            occ_type: str = self.__direction_abbrev_dict[occupancy_type]
        except KeyError:
            occ_type = occupancy_type

        return occ_type

    def __build_direction_abbreviations_dict(self) -> dict:
        """Builds a dictionary from an Excel spreadsheet that converts 'NorthWest' to 'NW'.

        Returns
        -------
        direction_abbrev_dict : dict
        """
        with resources.path(
            "redcaputilities.data", "direction_abbreviations.xlsx"
        ) as excel_filename:  # pragma: no cover
            if not os.path.exists(excel_filename):
                raise FileNotFoundError(f"Unable to find {excel_filename}.")

            direction_abbrev: pandas.DataFrame = pandas.read_excel(excel_filename)

            if direction_abbrev is None or not isinstance(
                direction_abbrev, pandas.DataFrame
            ):  # pragma: no cover
                raise OSError(f"Unable to read {excel_filename}.")

            # Convert to dictionary: https://stackoverflow.com/a/18695700/18749636
            direction_abbrev_dict: dict = direction_abbrev.set_index("Direction Name")[
                "Direction Abbreviation"
            ].to_dict()

            return direction_abbrev_dict

    def __build_street_abbreviations_dict(self) -> dict:
        """Builds a dictionary from an Excel spreadsheet that converts 'Street' to 'ST'.

        Returns
        -------
        street_abbrev_dict : dict
        """
        with resources.path(
            "redcaputilities.data", "street_abbreviations.xlsx"
        ) as excel_filename:  # pragma: no cover
            if not os.path.exists(excel_filename):
                raise FileNotFoundError(f"Unable to find {excel_filename}.")

            street_abbrev: pandas.DataFrame = pandas.read_excel(excel_filename)

            if street_abbrev is None or not isinstance(
                street_abbrev, pandas.DataFrame
            ):  # pragma: no cover
                raise OSError(f"Unable to read {excel_filename}.")

            # Convert to dictionary: https://stackoverflow.com/a/18695700/18749636
            street_abbrev_dict: dict = street_abbrev.set_index(
                "Commonly Used Street Suffix or Abbreviation"
            )["Postal Service Standard Suffix Abbreviation"].to_dict()

            return street_abbrev_dict

    def __build_unit_abbreviations_dict(self) -> dict:
        """Builds a dictionary from an Excel spreadsheet that converts 'Apartment' to 'APT'.

        Returns
        -------
        street_abbrev_dict : dict
        """
        with resources.path(
            "redcaputilities.data", "unit_abbreviations.xlsx"
        ) as excel_filename:  # pragma: no cover
            if not os.path.exists(excel_filename):
                raise FileNotFoundError(f"Unable to find {excel_filename}.")

            unit_abbrev: pandas.DataFrame = pandas.read_excel(excel_filename)

            if unit_abbrev is None or not isinstance(
                unit_abbrev, pandas.DataFrame
            ):  # pragma: no cover
                raise OSError(f"Unable to read {excel_filename}.")

            # Convert to dictionary: https://stackoverflow.com/a/18695700/18749636
            unit_abbrev_dict: dict = unit_abbrev.set_index("Unit designator")[
                "Abbreviation"
            ].to_dict()

            return unit_abbrev_dict

    def __clean_text(self, text: str) -> str:
        """Trims, removes punctuation & converts to uppercase.

        Parameters
        ----------
        text : str

        Returns
        -------
        text_cleaned : str
        """
        if not isinstance(text, str):
            raise TypeError("Input 'text' is not the expected string.")

        # Remove punctuation.
        text = text.translate(str.maketrans("", "", string.punctuation))

        # Remove whitespace.
        text = text.strip()

        return text.upper()

    def standardize_street_address(
        self, address: Union[str, list, pandas.Series]
    ) -> Union[str, list, pandas.Series]:
        """Standardizes street address according to USPS rules.

        Parameters
        ----------
        address : Union[str, list, pandas.Series]

        Returns
        -------
        address_standardized : Union[str, list, pandas.Series]
        """
        if isinstance(address, list):
            addresses_standardized: list = []

            for this_address in address:
                addresses_standardized.append(
                    self.standardize_street_address(this_address)
                )

            return addresses_standardized

        if isinstance(address, pandas.Series):
            addresses_standardized: list = []

            for this_address in address:
                addresses_standardized.append(
                    self.standardize_street_address(this_address)
                )

            return pandas.Series(addresses_standardized)

        if not isinstance(address, str):
            # Return empty string.
            return ""

        try:
            parsed_address: tuple = usaddress.tag(address)
            parsed_address_dict: collections.OrderedDict = parsed_address[0]
        except usaddress.RepeatedLabelError:
            # Then we can't parse this address.
            return address.strip().upper()

        # Handle PO Box first.
        if "USPSBoxType" in parsed_address_dict and "USPSBoxID" in parsed_address_dict:
            return (
                self.__clean_text(parsed_address_dict["USPSBoxType"])
                + " "
                + self.__clean_text(parsed_address_dict["USPSBoxID"])
            )

        address_standardized: str = ""

        if "AddressNumber" in parsed_address_dict:
            address_standardized += (
                self.__clean_text(parsed_address_dict["AddressNumber"]) + " "
            )

        if "StreetNamePreDirectional" in parsed_address_dict:
            address_standardized += (
                self.__abbreviate_direction(
                    parsed_address_dict["StreetNamePreDirectional"]
                )
                + " "
            )

        if "StreetName" in parsed_address_dict:
            address_standardized += (
                self.__clean_text(parsed_address_dict["StreetName"]) + " "
            )

        if "StreetNamePostType" in parsed_address_dict:
            address_standardized += (
                self.__abbreviate_street_type(parsed_address_dict["StreetNamePostType"])
                + " "
            )

        if "OccupancyIdentifier" in parsed_address_dict:
            if "OccupancyType" in parsed_address_dict:
                unit_type: str = self.__abbreviate_unit_type(
                    parsed_address_dict["OccupancyType"]
                )
            else:
                unit_type = "APT"

            address_standardized += (
                unit_type
                + " "
                + self.__clean_text(parsed_address_dict["OccupancyIdentifier"])
            )

        return address_standardized.strip()
