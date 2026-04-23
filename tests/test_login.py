import pytest
import allure

from helpers.stellarburgers_api import StellarBurgersAPI

@allure.feature('Авторизация пользователя')
@allure.story('API‑тесты авторизации пользователя')
class TestUserLogin:

    @allure.title('Успешная авторизация пользователя')
    @allure.description(
        'Проверяет успешную авторизацию зарегистрированного пользователя '
        'с корректными учётными данными'
    )
    def test_login_success(self, api_client):
        with allure.step('Создание тестового пользователя'):
            registration_payload = {
                "email": api_client.generate_random_email(),
                "password": "strongpassword123",
                "name": "TestUser"
            }
            api_client.create_user(registration_payload)

        with allure.step('Формирование данных для авторизации'):
            login_payload = {
                "email": registration_payload['email'],
                "password": "strongpassword123"
            }

        with allure.step('Отправка запроса на авторизацию'):
            response = api_client.login_user(login_payload)

        with allure.step('Проверка статуса ответа (200 OK)'):
            assert response.status_code == 200, \
                f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"

        with allure.step('Проверка успешности операции и наличия обязательных полей'):
            response_data = response.json()
            assert response_data.get("success") is True
            assert "accessToken" in response_data
            assert "refreshToken" in response_data
            assert "user" in response_data

        with allure.step('Проверка корректности данных пользователя в ответе'):
            assert response_data["user"]["email"] == registration_payload["email"]

    @allure.title('Авторизация с некорректным email')
    @allure.description(
        'Проверяет ответ API при попытке авторизации с несуществующим email'
    )
    def test_login_invalid_email(self, api_client):
        with allure.step('Формирование данных с некорректным email'):
            login_payload = {
                "email": "invalid-email@test.com",
                "password": "strongpassword123"
            }

        with allure.step('Отправка запроса на авторизацию'):
            response = api_client.login_user(login_payload)

        with allure.step('Проверка статуса ответа (401 Unauthorized)'):
            assert response.status_code == 401, \
                f"Ожидался код 401 получен {response.status_code}. Ответ: {response.text}"

        with allure.step('Проверка сообщения об ошибке'):
            response_data = response.json()
            assert response_data.get("success") is False
            assert response_data.get("message") == "email or password are incorrect"

    @allure.title('Авторизация с неверным паролем')
    @allure.description(
        'Проверяет ответ API при попытке авторизации с неверным паролем '
        'для существующего пользователя'
    )
    def test_login_invalid_password(self, api_client):
        with allure.step('Создание тестового пользователя'):
            registration_payload = {
                "email": api_client.generate_random_email(),
                "password": "strongpassword123",
                "name": "TestUser"
            }
            api_client.create_user(registration_payload)

        with allure.step('Формирование данных с неверным паролем'):
            login_payload = {
                "email": registration_payload['email'],
                "password": "wrongpassword123"
            }

        with allure.step('Отправка запроса на авторизацию'):
            response = api_client.login_user(login_payload)

        with allure.step('Проверка статуса ответа (401 Unauthorized)'):
            assert response.status_code == 401, \
                f"Ожидался код 401, получен {response.status_code}. Ответ: {response.text}"

        with allure.step('Проверка сообщения об ошибке'):
            response_data = response.json()
            assert response_data.get("success") is False
            assert response_data.get("message") == "email or password are incorrect"

    @allure.title('Авторизация с отсутствующими полями')
    @allure.description(
        'Проверяет ответ API при отправке запроса на авторизацию '
        'без обязательных полей (email или password)'
    )
    def test_login_missing_fields(self, api_client):
        with allure.step('Тест на отсутствие поля email'):
            response = api_client.login_user({"password": "password123"})
            assert response.status_code == 401, \
                f"Ожидался код 401, получен {response.status_code}. Ответ: {response.text}"

        with allure.step('Тест на отсутствие поля password'):
            response = api_client.login_user({"email": "test@test.com"})
            assert response.status_code == 401, \
                f"Ожидался код 401, получен {response.status_code}. Ответ: {response.text}"

    @allure.title('Авторизация с пустыми полями')
    @allure.description(
        'Проверяет ответ API при отправке запроса на авторизацию '
        'с пустыми значениями email и password'
    )
    def test_login_empty_fields(self, api_client):
        with allure.step('Отправка запроса с пустыми email и password'):
            response = api_client.login_user({"email": "", "password": ""})

        with allure.step('Проверка статуса ответа (401 Unauthorized)'):
            assert response.status_code == 401, \
                f"Ожидался код 401, получен {response.status_code}. Ответ: {response.text}"

    @allure.title('Авторизация с некорректным форматом email')
    @allure.description(
        'Проверяет ответ API при отправке запроса на авторизацию '
        'с email в некорректном формате'
    )
    def test_login_incorrect_format(self, api_client):
        with allure.step('Формирование данных с некорректным форматом email'):
            response = api_client.login_user({
                "email": "invalid_email",
                "password": "password123"
            })

        with allure.step('Проверка статуса ответа (401 Unauthorized)'):
            assert response.status_code == 401, \
                f"Ожидался код 401, получен {response.status_code}. Ответ: {response.text}"
