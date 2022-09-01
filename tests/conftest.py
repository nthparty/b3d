"""
All fixtures used by test functions
"""
import random
import string
import pytest
from tests import utils


@pytest.fixture
def generate_tag():
    """
    Generate a unique tag for each test
    """
    yield {
        "Key": "Name",
        "Value": f"B3DTEST_{''.join(random.choice(string.ascii_lowercase) for _ in range(10))}"
    }

    utils.cleanup_terraform_files_on_disk()
