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
        self, input_string: Union[str, list, pandas.Series]
    ) -> Union[str, list]:
        """Process a list or series of phone numbers.

        Parameters
        ----------
        input_string : Phone numbers, either one str, in a list or as a pandas.Series

        Returns
        -------
        cleaned_up_phones : Same form as the input: str or list
        """
        if not self.__valid:
            raise RuntimeError("Unable to execute method without token.")

        if isinstance(input_string, list):
            cleaned_up_phones = []

            for this_string in input_string:
                if self.validate_one_phone_number(this_string):
                    cleaned_up_phones.append(this_string)
                else:
                    cleaned_up_phones.append("")

            return cleaned_up_phones

        if input_string is None:
            return ""

        if isinstance(input_string, pandas.Series):
            input_string = input_string[0]

        if not isinstance(input_string, str):
            raise TypeError("Argument 'input_string' is neither string nor list.")

        if self.validate_one_phone_number(input_string):
            return input_string
        else:
            return ""
