"""
Module: contains the Veriphone class, which handles querying the Veriphone online service.
"""
import configparser
import json
import logging
import os.path
import pandas
import platform
import requests
from typing import Union
from redcaputilities.logging import setup_logging


class Veriphone:
    """Handles querying the Veriphone online service."""

    __url: str = "https://api.veriphone.io/v2/verify"

    def __init__(self):
        """Creates instance of Veriphone class."""
        self.__log: logging.Logger = setup_logging(log_filename="veriphone_api.log")
        self.__valid: bool = False
        self.__token: Union[str, None] = self.__read_config_file()

    def __path_to_secrets(self) -> str:
        """Returns machine-dependent path to secrets files.

        Returns
        -------
        secrets_dir : str
        """
        secrets_dir: str = r"C:\.ssh"
        machine_name: str = platform.node()

        if machine_name == "medicinedb5p01":
            secrets_dir = r"F:\.ssh"

        return secrets_dir

    def __read_config_file(self) -> str:
        """Reads the Veriphone token."""
        token: str = ""
        secrets_dir: str = self.__path_to_secrets()
        full_filename: str = os.path.join(secrets_dir, r"veriphone api token.txt")

        if not os.path.isfile(full_filename):
            self.__log.error('Unable to find key file "' + full_filename + '".')
            raise RuntimeError("Unable to find key file.")

        config = configparser.ConfigParser()

        try:
            config.read(full_filename)
            token = config.get("VERIPHONE", "VERIPHONE_TOKEN")
            self.__valid = True
        except:
            pass

        return token

    def validate_one_phone_number(self, phone_number: str) -> bool:
        """Sends phone number in question to Veriphone service.

        Parameters
        ----------
        phone_number : str

        Returns
        -------
        valid : bool
        """
        if not self.__valid:
            raise RuntimeError("Unable to execute method without token.")

        valid: bool = False

        if not isinstance(phone_number, str):
            self.__log.error("Phone number provided was not a str.")
            return valid

        url_extended: str = (
            self.__url + "?phone=" + phone_number + "&key=" + self.__token
        )
        response = requests.get(url_extended)

        if not isinstance(response, requests.Response):
            self.__log.error("Unable to create records; no 'response' object.")
            return False

        # If the input's invalid, then call the phone number invalid.
        # Code 400 => Input parameter missing or not valid.
        # Code 401 => Key parameter is missing or not valid.
        # https://veriphone.io/docs/v2
        if response.status_code == 400 or response.status_code == 401 :
            self.__log.error("Invalid number:", response.text)
            return False

        # If we've used all our free credits for the month, we'll receive a 402 error.
        # That doesn't mean the phone number is invalid, so to avoid deleting possibly
        # valid numbers, return True.
        if response.status_code == 402:
            self.__log.error("Out of Veriphone credits:", response.text)
            return True

        # Same here--log for further investigation, but don't discard the number.
        if response.status_code != 200:
            self.__log.error(
                "Unable to request validation because: '%s'.", response.text
            )
            return True

        # Convert the string that *looks* like a dict to an actual dict object.
        response_dict: dict = json.loads(response.text)

        if "phone_valid" in response_dict:
            valid = response_dict["phone_valid"]

        return valid

    def validate_phone_numbers(
        self, raw_phone_numbers: Union[str, list, pandas.Series]
    ) -> Union[str, list, pandas.Series]:
        """Process a list or series of phone numbers.

        Parameters
        ----------
        raw_phone_numbers : Phone numbers, either one str, in a list or as a pandas.Series

        Returns
        -------
        validated_phone_numbers : Same form as the input: str or list or Series
        """
        if not self.__valid:
            raise RuntimeError("Unable to execute method without token.")

        if raw_phone_numbers is None:
            return ""

        if isinstance(raw_phone_numbers, list):
            validated_phone_numbers = raw_phone_numbers[:]

            for index, this_string in enumerate(raw_phone_numbers):
                if not self.validate_one_phone_number(this_string):
                    validated_phone_numbers[index] = ""

            return validated_phone_numbers

        if isinstance(raw_phone_numbers, pandas.Series):
            validated_phone_numbers = pandas.Series(raw_phone_numbers)

            for index, this_string in enumerate(raw_phone_numbers):
                if not self.validate_one_phone_number(this_string):
                    validated_phone_numbers[index] = ""

            return validated_phone_numbers

        if not isinstance(raw_phone_numbers, str):
            raise TypeError("Argument 'raw_phone_numbers' is neither string nor list nor Series.")

        if self.validate_one_phone_number(raw_phone_numbers):
            return raw_phone_numbers
        else:
            return ""
