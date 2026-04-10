import pytest

from helpers.stellarburgers_api import StellarBurgersAPI

class TestUserRegistration:

    def test_create_user_success(self, api_client):
        payload = {
            "email": api_client.generate_random_email(),
            "password": "strongpassword123",
            "name": api_client.generate_random_name()
        }
        
        response = api_client.create_user(payload)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data.get("success") is True
        assert "user" in response_data
        assert "accessToken" in response_data
        assert "refreshToken" in response_data

        # Проверяем получение данных пользователя
        headers = {
            "Authorization": response_data['accessToken']
        }

        user_response = api_client.get_user(headers)
        
        assert user_response.status_code == 200
        user_data = user_response.json()
        assert user_data.get("success") is True
        assert user_data["user"]["email"] == payload["email"]
        assert user_data["user"]["name"] == payload["name"]

    