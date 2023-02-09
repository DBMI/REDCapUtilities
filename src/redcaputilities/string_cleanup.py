"""
    Allows other projects to easily use these string cleanup utilities.
"""
from typing import Union

import dateutil.parser


def clean_up_date(input_string: Union[str, list]) -> Union[str, list]:
    """Ensures dates are in yyyy-mm-dd format.

    Parameters
    ----------
    input_string : Either a string or a list of strings

    Returns
    -------
    cleaned_up_date : Same form as the input: string or list
    """

    if isinstance(input_string, list):
        cleaned_up_dates = []

        for this_string in input_string:
            cleaned_up_dates.append(clean_up_date(this_string))

        return cleaned_up_dates

    if not isinstance(input_string, str):
        raise TypeError("Argument 'input_string' is neither string nor list.")

    # Let's not reinvent the wheel. Use this flexible library.
    try:
        datetime_obj = dateutil.parser.parse(input_string)
        cleaned_up_date = datetime_obj.strftime("%Y-%m-%d")
    except dateutil.parser.ParserError:
        cleaned_up_date = ""

    return cleaned_up_date


def clean_up_phone(input_string: Union[str, list]) -> Union[str, list]:
    """Ensures phone numbers are in ###-###-#### format. Detects & removes likely dummy numbers like "9999999999".

    Parameters
    ----------
    input_string : Either a string or a list of strings

    Returns
    -------
    cleaned_up_phone : Same form as the input: string or list

    """
    if isinstance(input_string, list):
        cleaned_up_phones = []

        for this_string in input_string:
            cleaned_up_phones.append(clean_up_phone(this_string))

        return cleaned_up_phones

    if not isinstance(input_string, str):
        raise TypeError("Argument 'input_string' is neither string nor list.")

    if input_string.upper().strip() == "NULL" or input_string.upper().strip() == "NONE":
        return ""

    numeric_filter = filter(str.isdigit, input_string)
    numeric_string = "".join(numeric_filter)

    if numeric_string in (
        "0000000000",
        "10000000000",
        "9999999999",
        "19999999999",
        "1111111111",
    ):
        return ""

    if numeric_string.startswith("1") and len(numeric_string) == 11:  # 1YYYXXXZZZZ
        numeric_string = numeric_string[1:]

    if len(numeric_string) != 10:
        return input_string

    prefix = numeric_string[0:3]
    exchange = numeric_string[3:6]
    rest = numeric_string[6:10]
    return f"{prefix}-{exchange}-{rest}"


def clean_up_time(input_string: Union[str, list]) -> Union[str, list]:
    """Ensures times are in HH:MM:SS format.

    Parameters
    ----------
    input_string : Either a string or a list of strings

    Returns
    -------
    cleaned_up_time : Same form as the input: string or list

    """
    if isinstance(input_string, list):
        cleaned_up_times = []

        for this_string in input_string:
            cleaned_up_times.append(clean_up_time(this_string))

        return cleaned_up_times

    if not isinstance(input_string, str):
        raise TypeError("Argument 'input_string' is neither string nor list.")

    # Let's not reinvent the wheel. Use this flexible library.
    try:
        datetime_obj = dateutil.parser.parse(input_string)
        cleaned_up_time = datetime_obj.strftime("%H:%M:%S")
    except dateutil.parser.ParserError:
        cleaned_up_time = ""

    return cleaned_up_time
