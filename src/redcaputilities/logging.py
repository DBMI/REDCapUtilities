"""
    Allows other projects to easily use logging.
"""
import logging
import os
import sys
from datetime import datetime
from typing import Union

from src.redcaputilities.directories import ensure_output_path_exists


def patient_data_directory() -> str:
    """Looks up the directory designated safe for patient data.

    Returns
    -------
    patient_data_dir : str

    """

    patient_data_dir = os.getenv("PATIENT_DATA")

    if not patient_data_dir:  # pragma: no cover
        patient_data_dir = r"F:\AoU_v2"

    return patient_data_dir


def setup_logging(log_filename: Union[str, None] = None) -> logging.Logger:
    """

    Parameters
    ----------
    log_filename : Optional str Just the name (not path) of the log file.

    Returns
    -------
    logger : logging.Logger object to be used in calling routine.

    """
    # Clear up any old stuff.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Put log files in proper directory.
    patient_data_dir = patient_data_directory()
    logs_directory = os.path.join(patient_data_dir, "logs")

    if not isinstance(log_filename, str):
        now = datetime.today().strftime("%Y%m%d_%H%M%S")
        log_filename = f"redcap_{now}.log"

    log_full_filename = os.path.join(logs_directory, log_filename)
    ensure_output_path_exists(log_full_filename)

    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_format)

    logfile_handler = logging.FileHandler(filename=log_full_filename)
    logfile_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logfile_handler.setFormatter(logfile_format)

    logger.addHandler(console_handler)
    logger.addHandler(logfile_handler)
    logger.setLevel(logging.INFO)
    return logger
