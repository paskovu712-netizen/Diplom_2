import pytest

from helpers.stellarburgers_api import StellarBurgersAPI

class TestOrders:
    @pytest.fixture
    def registered_user(self, api_client):
        payload = {
            "email": api_client.generate_random_email(),
            "password": "strongpassword123",
            "name": "TestUser"
        }
        api_client.create_user(payload)
        login_response = api_client.login_user({
            "email": payload['email'],
            "password": "strongpassword123"
        })
        data = login_response.json()
        return {
            "token": data['accessToken'],
            "email": payload['email']
        }

    def test_create_order_authorized(self, api_client, registered_user):
        payload = {
            "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
        }
        
        headers = {
            "Authorization": registered_user['token']
        }
        response = api_client.create_order(payload, headers) 
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'name' in data
        assert 'order' in data
        assert 'number' in data['order']

    def test_create_order_unauthorized(self, api_client):
        payload = {
            "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
        }
        
        response = api_client.create_order(payload, "")
        assert response.status_code == 200

    def test_create_order_no_ingredients(self, api_client, registered_user):
        payload = {}
        headers = {
            "Authorization": registered_user['token']
        }
        response = api_client.create_order(payload, headers)
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert data['message'] == "Ingredient ids must be provided"

    def test_create_order_invalid_ingredient(self, api_client, registered_user):
        payload = {
            "ingredients": ["invalid_id"]
        }
        headers = {
            "Authorization": registered_user['token']
        }
        response = api_client.create_order(payload, headers)
        assert response.status_code == 500

    def test_create_order_empty_ingredients(self, api_client, registered_user):
        payload = {
            "ingredients": []
        }
        headers = {
            "Authorization": registered_user['token']
        }

        response = api_client.create_order(payload, headers)
        assert response.status_code == 400
        data = response.json()
        assert data['success'] is False
        assert data['message'] == "Ingredient ids must be provided"


