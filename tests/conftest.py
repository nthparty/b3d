import random
import string
import pytest


@pytest.fixture
def generate_tag():
    """
    Generate a unique tag for each test
    """
    return {
        "Key": "b3d-test",
        "Value": "".join(random.choice(string.ascii_lowercase) for _ in range(10))
    }



