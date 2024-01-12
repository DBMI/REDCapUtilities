"""
    Allows other projects to easily use these string cleanup utilities.
"""
import re
from datetime import datetime as datetime
from typing import Union

import dateutil.parser
import pandas  # type: ignore[import]


def clean_up_date(
    input_string: Union[str, list, pandas.Series, datetime]
) -> Union[str, list]:
    """Ensures dates are in yyyy-mm-dd format.

    Parameters
    ----------
    input_string : Handles string or datetime object, either alone, in a list or as a pandas.Series

    Returns
    -------
    cleaned_up_date : Same form as the input: string or list
    """

    if isinstance(input_string, list):
        cleaned_up_dates = []

        for this_string in input_string:
            cleaned_up_dates.append(clean_up_date(this_string))

        return cleaned_up_dates

    if input_string is None:
        return ""

    if isinstance(input_string, pandas.Series):
        input_string = input_string[0]

    if isinstance(input_string, datetime):
        return input_string.strftime("%Y-%m-%d")

    if not isinstance(input_string, str):
        raise TypeError("Argument 'input_string' is neither string nor list.")

    # Let's not reinvent the wheel. Use this flexible library.
    try:
        datetime_obj = dateutil.parser.parse(input_string)
        cleaned_up_date = datetime_obj.strftime("%Y-%m-%d")
    except dateutil.parser.ParserError:
        cleaned_up_date = ""

    return cleaned_up_date


def clean_up_email(input_string: Union[str, list, pandas.Series]) -> Union[str, list]:
    """Removes emails like 'None' or 'none@ucsd.edu'.

    Parameters
    ----------
    input_string : Handles string email address, either alone, in a list or as a pandas.Series

    Returns
    -------
    cleaned_up_email : Same form as the input: string or list
    """

    if isinstance(input_string, list):
        cleaned_up_emails = []

        for this_string in input_string:
            cleaned_up_emails.append(clean_up_email(this_string))

        return cleaned_up_emails

    if input_string is None:
        return ""

    if isinstance(input_string, pandas.Series):
        input_string = input_string[0]

    if not isinstance(input_string, str):
        raise TypeError("Argument 'input_string' is neither string nor list.")

    #   Remove None, NONE, etc. but not if it's part of a larger string
    cleaned_up_email = re.sub(
        r"\b(decline|declined|none|refuse|refused|unk|unknown)\b",
        "",
        input_string,
        flags=re.IGNORECASE,
    )

    #   Remove partial address like '@ucsd.edu'
    #   (which may be left over from previous step if address was 'none@ucsd.edu'.)
    cleaned_up_email = re.sub(r"^@.*", "", cleaned_up_email)

    return cleaned_up_email


def clean_up_phone(input_string: Union[str, list, pandas.Series]) -> Union[str, list]:
    """Ensures phone numbers are in ###-###-#### format. Detects & removes likely dummy numbers like "9999999999".

    Parameters
    ----------
    input_string : Either a string or a list of strings or a pandas.Series

    Returns
    -------
    cleaned_up_phone : Same form as the input: string or list

    """
    if isinstance(input_string, list):
        cleaned_up_phones = []

        for this_string in input_string:
            cleaned_up_phones.append(clean_up_phone(this_string))

        return cleaned_up_phones

    if input_string is None:
        return ""

    if isinstance(input_string, pandas.Series):
        input_string = input_string[0]

    if not isinstance(input_string, str):
        raise TypeError("Argument 'input_string' is neither string nor list.")

    input_string = input_string.strip()

    if input_string.upper() == "NULL" or input_string.upper() == "NONE":
        return ""

    numeric_filter = filter(str.isdigit, input_string)
    numeric_string = "".join(numeric_filter)

    #   If the original string contained letters in place of numbers,
    #   restricting it to only digits will result in length < 10.
    if len(numeric_string) < 10:
        return ""

    if numeric_string in (
        "0000000000",
        "10000000000",
        "9999999999",
        "19999999999",
        "1111111111",
    ):
        return ""

    #   Get rid of numbers like 619-000-0000.
    if "0000" in numeric_string:
        return ""

    if numeric_string.startswith("1") and len(numeric_string) == 11:  # 1YYYXXXZZZZ
        numeric_string = numeric_string[1:]

    if len(numeric_string) != 10:
        return input_string

    prefix = numeric_string[0:3]
    exchange = numeric_string[3:6]
    rest = numeric_string[6:10]
    return f"{prefix}-{exchange}-{rest}"


def clean_up_string(
    input_string: Union[str, list, pandas.Series], strings_to_ignore: list
) -> Union[str, list]:
    """Blank strings on the 'ignore' list.

    Parameters
    ----------
    input_string : str string, either alone, in a list or as a pandas.Series
    strings_to_ignore : list of strs

    Returns
    -------
    cleaned_up_strings : Same form as the input: string, list or pandas.Series
    """

    if not isinstance(strings_to_ignore, list):
        raise TypeError('Argument "strings_to_ignore" is not the expected list.')

    if isinstance(input_string, list):
        cleaned_up_strings = []

        for this_string in input_string:
            cleaned_up_strings.append(
                clean_up_string(
                    input_string=this_string, strings_to_ignore=strings_to_ignore
                )
            )

        return cleaned_up_strings

    if input_string is None:
        return ""

    if isinstance(input_string, pandas.Series):
        input_string = input_string[0]

    if not isinstance(input_string, str):
        return ""

    cleaned_up_string = input_string

    #   Remove any string on the 'ignored' list.
    if input_string in strings_to_ignore:
        cleaned_up_string = ""

    return cleaned_up_string


def clean_up_time(input_string: Union[str, list, pandas.Series]) -> Union[str, list]:
    """Ensures times are in HH:MM:SS format.

    Parameters
    ----------
    input_string : Either a string or a list of strings or a pandas.Series

    Returns
    -------
    cleaned_up_time : Same form as the input: string or list

    """
    if isinstance(input_string, list):
        cleaned_up_times = []

        for this_string in input_string:
            cleaned_up_times.append(clean_up_time(this_string))

        return cleaned_up_times

    if input_string is None:
        return ""

    if isinstance(input_string, pandas.Series):
        input_string = input_string[0]

    if not isinstance(input_string, str):
        raise TypeError("Argument 'input_string' is neither string nor list.")

    # Let's not reinvent the wheel. Use this flexible library.
    try:
        datetime_obj = dateutil.parser.parse(input_string)
        cleaned_up_time = datetime_obj.strftime("%H:%M:%S")
    except dateutil.parser.ParserError:
        cleaned_up_time = ""

    return cleaned_up_time


def extend_street_abbreviations(street_address: str) -> str:
    """Converts 'St' or 'Ave' to 'Street' and 'Avenue'

    Parameters
    ----------
    street_address : str

    Returns
    -------
    full_street_address : str
    """
    if not isinstance(street_address, str):
        return street_address

    #   Trim whitespace & convert to lower case.
    street_address = street_address.strip().lower()

    #   https://gis.stackexchange.com/q/336221
    abbreviations: dict = {
        "aly": "Alley",
        "ave": "Avenue",
        "blvd": "Boulevard",
        "blv": "Boulevard",
        "cir": "Circle",
        "ct": "Court",
        "cv": "Cove",
        "cyn": "Canyon",
        "dr": "Drive",
        "expy": "Expressway",
        "hwy": "Highway",
        "gln": "Glen",
        "ln": "Lane",
        "pkwy": "Parkway",
        "pl": "Place",
        "pt": "Point",
        "rd": "Road",
        "sq": "Square",
        "st": "Street",
        "ter": "Terrace",
        "trl": "Trail",
        "tr": "Trail",
        "wy": "Way",
    }

    for key in abbreviations:
        if key in street_address:
            #   Remove punctuation associated with abbreviation.
            street_address = re.sub(key + r"\.", key, street_address)

            #   Replace keys if they are a full word.
            street_address = re.sub(
                r"\b" + key + r"\b", abbreviations[key], street_address
            )

    #   Restore to Title Case.
    street_address = street_address.title()

    #   Undo conversion of 1st, 2nd, 3rd, 4th....
    street_address = re.sub(r"(\d)St", r"\1st", street_address)
    street_address = re.sub(r"(\d)Nd", r"\1nd", street_address)
    street_address = re.sub(r"(\d)Rd", r"\1rd", street_address)
    street_address = re.sub(r"(\d)Th", r"\1th", street_address)
    return street_address
