"""
Tests for the logging utility functions.
"""

import logging
import os

from src.redcaputilities.my_logging import patient_data_directory, setup_logging


def test_logging_setup():
    logs_path = os.path.join(patient_data_directory(), "logs")
    target_log_file = os.path.join(logs_path, "test.log")

    if os.path.exists(target_log_file):
        os.remove(target_log_file)

    # Call for log to be setup.
    logger = setup_logging(log_filename="test.log")
    assert isinstance(logger, logging.Logger)
    logger.info("Hello, world!")

    # Check that file now exists.
    assert os.path.exists(target_log_file)
    #
    # Try with default filename.
    #
    logger = setup_logging()
    logger.info("Hello, world!")
    target_log_file = os.path.join(logs_path, "redcap_test_logging.log")
    assert os.path.exists(target_log_file)


def test_patient_data_directory(tmp_path):
    pat_data_dir = patient_data_directory()
    assert isinstance(pat_data_dir, str)
    assert pat_data_dir == tmp_path
