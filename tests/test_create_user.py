import pytest
import allure

from helpers.stellarburgers_api import StellarBurgersAPI

@allure.feature('Регистрация пользователя')
@allure.story('API-тесты регистрации и получения данных пользователя')
class TestUserRegistration:

    @allure.title('Успешная регистрация пользователя через API')
    @allure.description(
        'Проверяет успешную регистрацию нового пользователя через API, '
        'а также получение данных зарегистрированного пользователя'
    )
    def test_create_user_success(self, api_client):
        with allure.step('Подготовка тестовых данных для регистрации'):
            payload = {
                "email": api_client.generate_random_email(),
                "password": "strongpassword123",
                "name": api_client.generate_random_name()
            }

        with allure.step('Отправка запроса на регистрацию пользователя'):
            response = api_client.create_user(payload)

        with allure.step('Проверка статуса ответа и успешности операции'):
            assert response.status_code == 200, \
                f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"
            response_data = response.json()
            assert response_data.get("success") is True

        with allure.step('Проверка наличия обязательных полей в ответе'):
            assert "user" in response_data
            assert "accessToken" in response_data
            assert "refreshToken" in response_data

        with allure.step('Формирование заголовков с токеном авторизации'):
            headers = {
                "Authorization": response_data['accessToken']
            }

        with allure.step('Запрос данных пользователя'):
            user_response = api_client.get_user(headers)

        with allure.step('Проверка статуса ответа при получении данных пользователя'):
            assert user_response.status_code == 200, \
                f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"

        with allure.step('Проверка корректности полученных данных пользователя'):
            user_data = user_response.json()
            assert user_data.get("success") is True
            assert user_data["user"]["email"] == payload["email"]
            assert user_data["user"]["name"] == payload["name"]
    