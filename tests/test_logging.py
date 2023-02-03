"""
    Tests for the logging utility functions.
"""
from datetime import datetime
from fnmatch import fnmatch
import logging
import os
from src.redcaputilities.logging import patient_data_directory, setup_logging


def test_logging_setup(secure_data_directory):
    logs_path = os.path.join(secure_data_directory, 'logs')
    target_log_file = os.path.join(logs_path, "test.log")

    if os.path.exists(target_log_file):
        os.remove(target_log_file)

    # Call for log to be setup.
    logger = setup_logging(log_filename="test.log")
    assert isinstance(logger, logging.Logger)

    # Check that file now exists.
    assert os.path.exists(target_log_file)
    #
    # Try default filename.
    #
    setup_logging()

    today = datetime.today().strftime("%Y%m%d")
    pattern = 'redcap_' + today + '*.log'

    # Look for file (which will have a filename containing timestamp.)
    assert any(fnmatch(file, pattern) for file in os.listdir(logs_path))


def test_patient_data_directory(secure_data_directory):
    pat_data_dir = patient_data_directory()
    assert isinstance(pat_data_dir, str)
    assert pat_data_dir == secure_data_directory
