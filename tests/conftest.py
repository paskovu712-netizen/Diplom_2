# conftest.py
import pytest
import allure

from helpers.stellarburgers_api import StellarBurgersAPI

@pytest.fixture(scope="function")
def api_client():
    client = StellarBurgersAPI()
    yield client
    client.teardown()

@pytest.fixture
def registered_user(api_client):
    with allure.step('Создание тестового пользователя'):
        payload = {
            "email": api_client.generate_random_email(),
            "password": "strongpassword123",
            "name": "TestUser"
        }
        api_client.create_user(payload)

    with allure.step('Авторизация пользователя и получение токена'):
        login_response = api_client.login_user({
            "email": payload['email'],
            "password": "strongpassword123"
        })
        data = login_response.json()

    return {
        "token": data['accessToken'],
        "email": payload['email']
    }
