import pytest

from helpers.stellarburgers_api import StellarBurgersAPI

class TestUserLogin:
    def test_login_success(self, api_client):
        # Создаем пользователя
        registration_payload = {
            "email": api_client.generate_random_email(),
            "password": "strongpassword123",
            "name": "TestUser"
        }
        api_client.create_user(registration_payload)
        
        # Пытаемся войти
        login_payload = {
            "email": registration_payload['email'],
            "password": "strongpassword123"
        }
        response = api_client.login_user(login_payload)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get("success") is True
        assert "accessToken" in response_data
        assert "refreshToken" in response_data
        assert "user" in response_data
        assert response_data["user"]["email"] == registration_payload["email"]

    def test_login_invalid_email(self, api_client):
        login_payload = {
            "email": "invalid-email@test.com",
            "password": "strongpassword123"
        }
        response = api_client.login_user(login_payload)
        
        assert response.status_code == 401
        response_data = response.json()
        assert response_data.get("success") is False
        assert response_data.get("message") == "email or password are incorrect"

    def test_login_invalid_password(self, api_client):
        # Создаем пользователя
        registration_payload = {
            "email": api_client.generate_random_email(),
            "password": "strongpassword123",
            "name": "TestUser"
        }
        api_client.create_user(registration_payload)
        
        # Пытаемся войти с неверным паролем
        login_payload = {
            "email": registration_payload['email'],
            "password": "wrongpassword123"
        }
        response = api_client.login_user(login_payload)
        
        assert response.status_code == 401
        response_data = response.json()
        assert response_data.get("success") is False
        assert response_data.get("message") == "email or password are incorrect"

    def test_login_missing_fields(self, api_client):
        # Тест на отсутствие email
        response = api_client.login_user({"password": "password123"})
        assert response.status_code == 401
        
        # Тест на отсутствие password
        response = api_client.login_user({"email": "test@test.com"})
        assert response.status_code == 401

    def test_login_empty_fields(self, api_client):
        # Тест на пустые поля
        response = api_client.login_user({"email": "", "password": ""})
        assert response.status_code == 401

    def test_login_incorrect_format(self, api_client):
        # Тест на некорректный формат email
        response = api_client.login_user({
            "email": "invalid_email",
            "password": "password123"
        })
        assert response.status_code == 401
