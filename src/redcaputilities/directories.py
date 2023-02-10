"""
    Allows other projects to easily use directory methods.
"""
import os


def ensure_output_path_exists(target_filename: str = "") -> None:
    """Make sure the directory to hold the target file is prepared.

    Parameters
    ----------
    target_filename : str Full path to location of file to be created.

    """
    if not isinstance(target_filename, str) or len(target_filename) == 0:
        raise TypeError("Target filename not supplied.")

    target_path = ""

    try:
        target_path = os.path.dirname(target_filename)

        if not target_path:  # pragma: no cover
            raise RuntimeError(
                f"Target path cannot be determined from filename '{target_filename}'."
            )

        if not os.path.exists(target_path):
            os.makedirs(target_path)
    except OSError as create_path_error:  # pragma: no cover
        raise OSError(
            f"Unable to create path: '{target_path}' "
            + f"because{str(create_path_error)}."
        ) from create_path_error
