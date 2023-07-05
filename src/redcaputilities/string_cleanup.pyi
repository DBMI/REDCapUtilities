from datetime import datetime as datetime
from typing import Union

import pandas  # type: ignore[import]

def clean_up_date(
    input_string: Union[str, list, pandas.Series]
) -> Union[str, list]: ...
def clean_up_phone(
    input_string: Union[str, list, pandas.Series]
) -> Union[str, list]: ...
def clean_up_time(
    input_string: Union[str, list, pandas.Series]
) -> Union[str, list]: ...
def extend_street_abbreviations(street_address: str) -> str: ...
