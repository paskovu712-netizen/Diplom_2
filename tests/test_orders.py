import pytest
import allure

from helpers.stellarburgers_api import StellarBurgersAPI

@allure.feature('Создание заказов')
@allure.story('API‑тесты создания заказов')
class TestOrders:
    @allure.title('Создание заказа авторизованным пользователем')
    @allure.description(
        'Проверяет успешное создание заказа авторизованным пользователем '
        'с указанием списка ингредиентов'
    )
    def test_create_order_authorized(self, api_client, registered_user):
        with allure.step('Формирование данных заказа с ингредиентами'):
            payload = {
                "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
            }

        with allure.step('Формирование заголовков с токеном авторизации'):
            headers = {
                "Authorization": registered_user['token']
            }

        with allure.step('Отправка запроса на создание заказа'):
            response = api_client.create_order(payload, headers)

        with allure.step('Проверка статуса ответа (200 OK)'):
            assert response.status_code == 200

        with allure.step('Проверка успешности операции и наличия обязательных полей в ответе'):
            data = response.json()
            assert data['success'] is True
            assert 'name' in data
            assert 'order' in data
            assert 'number' in data['order']

    @allure.title('Создание заказа неавторизованным пользователем')
    @allure.description(
        'Проверяет возможность создания заказа неавторизованным пользователем'
    )
    def test_create_order_unauthorized(self, api_client):
        with allure.step('Формирование данных заказа'):
            payload = {
                "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
            }

        with allure.step('Отправка запроса на создание заказа без авторизации'):
            response = api_client.create_order(payload, "")

        with allure.step('Проверка статуса ответа (200 OK)'):
            assert response.status_code == 200

    @allure.title('Создание заказа без указания ингредиентов')
    @allure.description(
        'Проверяет ответ API при попытке создания заказа '
        'без указания ингредиентов'
    )
    def test_create_order_no_ingredients(self, api_client, registered_user):
        with allure.step('Формирование пустого тела запроса'):
            payload = {}

        with allure.step('Формирование заголовков с токеном авторизации'):
            headers = {
                "Authorization": registered_user['token']
            }

        with allure.step('Отправка запроса на создание заказа'):
            response = api_client.create_order(payload, headers)

        with allure.step('Проверка статуса ответа (400 Bad Request)'):
            assert response.status_code == 400

        with allure.step('Проверка сообщения об ошибке'):
            data = response.json()
            assert data['success'] is False
            assert data['message'] == "Ingredient ids must be provided"

    @allure.title('Создание заказа с некорректным ID ингредиента')
    @allure.description(
        'Проверяет ответ API при попытке создания заказа '
        'с некорректным ID ингредиента'
    )
    def test_create_order_invalid_ingredient(self, api_client, registered_user):
        with allure.step('Формирование данных с некорректным ID ингредиента'):
            payload = {
                "ingredients": ["invalid_id"]
            }

        with allure.step('Формирование заголовков с токеном авторизации'):
            headers = {
                "Authorization": registered_user['token']
            }

        with allure.step('Отправка запроса на создание заказа'):
            response = api_client.create_order(payload, headers)

        with allure.step('Проверка статуса ответа (500 Internal Server Error)'):
            assert response.status_code == 500

    @allure.title('Создание заказа с пустым списком ингредиентов')
    @allure.description(
        'Проверяет ответ API при попытке создания заказа '
        'с пустым списком ингредиентов'
    )
    def test_create_order_empty_ingredients(self, api_client, registered_user):
        with allure.step('Формирование данных с пустым списком ингредиентов'):
            payload = {
                "ingredients": []
            }

        with allure.step('Формирование заголовков с токеном авторизации'):
            headers = {
                "Authorization": registered_user['token']
            }

        with allure.step('Отправка запроса на создание заказа'):
            response = api_client.create_order(payload, headers)

        with allure.step('Проверка статуса ответа (400 Bad Request)'):
            assert response.status_code == 400

        with allure.step('Проверка сообщения об ошибке'):
            data = response.json()
            assert data['success'] is False
            assert data['message'] == "Ingredient ids must be provided"


