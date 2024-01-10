import configparser
import logging
import os.path
import pandas
import platform
import requests
from typing import Union
from redcaputilities.logging import setup_logging

class Veriphone:
    __url: str = None

    def __init__(self) -> None:
        self.__log: logging.Logger = None
        self.__token: Union[str, None] = None
        self.__valid: bool = None
    def __path_to_secrets(self) -> str: ...
    def __read_config_file(self) -> str: ...
    def validate_one_phone_number(self, phone_number: str) -> bool: ...
    def validate_phone_numbers(
        self, input_string: Union[str, list, pandas.Series]
    ) -> Union[str, list, pandas.Series]: ...
