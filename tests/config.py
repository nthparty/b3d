"""
Tests-wide configuration parameters and methods
"""
import os
import logging
import logging.handlers
import datetime


TF_DEPLOYMENT_DIR = os.sep.join([os.path.dirname(os.path.realpath(__file__)), "terraform"])
AWS_REGION = "us-east-1"
AVAILABILITY_ZONE = "us-east-1a"
# Need an AMI ID for RunInstances API call
TEST_AMI_ID = "ami-0c4cfe9aec8b21224"
LOGFILE = "b3d-test.log"
LOGLEVEL = "INFO"
LOGGER = logging.getLogger("b3d.test")


def configure_logger():

    handler = logging.handlers.WatchedFileHandler(LOGFILE)
    handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    LOGGER.setLevel(LOGLEVEL)
    LOGGER.addHandler(handler)
    LOGGER.info(
        f"starting b3d tests {datetime.datetime.now().isoformat()}"
    )
