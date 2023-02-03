"""
    Allows other projects to easily use these numeric utilities.
"""


def is_even(value: int) -> bool:
    """Is the number even?
    Parameters
    ----------
    value : int

    Returns
    -------
    is_even : bool
    """
    if not isinstance(value, int):
        raise TypeError("Input 'value' is not the expected int.")

    return (value % 2) == 0
