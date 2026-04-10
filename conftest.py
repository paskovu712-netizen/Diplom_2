# conftest.py
import pytest

from helpers.stellarburgers_api import StellarBurgersAPI

@pytest.fixture(scope="function")
def api_client():
    client = StellarBurgersAPI()
    yield client
    client.teardown()
