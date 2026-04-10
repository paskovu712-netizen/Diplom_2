import requests
import json
import random
import string

from data.data import BASE_URL, ENDPOINTS

class StellarBurgersAPI:
    def __init__(self):
        self.base_url = BASE_URL
        self.users_to_delete = []  # Хранилище для созданных пользователей
        self.tokens = {}  # Хранилище токенов

    def create_user(self, user_data):
        url = ENDPOINTS["register"]        
        response = requests.post(url, json=user_data)
        if response.status_code == 200:
            data = response.json()
            self.users_to_delete.append(user_data['email'])
            self.tokens[user_data['email']] = {
                "accessToken": data['accessToken'],
                "refreshToken": data['refreshToken']
            }
        return response
    
    def login_user(self, user_data):
        url = ENDPOINTS["login"]
        return requests.post(url, json=user_data)

    def get_user(self, headers):
        url = ENDPOINTS["user"]
        return requests.get(url, headers=headers)

    def delete_user(self, email):
        url = ENDPOINTS["user"]
        accessToken = self.tokens[email]['accessToken']
        headers = {
            "Authorization": accessToken
        }
        return requests.delete(url, headers=headers)

    def logout(self, refresh_token):
        url = ENDPOINTS["logout"]
        payload = {
            "token": refresh_token
        }
        return requests.post(url, json=payload)

    def create_order(self, payload, header):
        url = ENDPOINTS["orders"]
        response = requests.post(url, payload, headers=header)
        return response

    def teardown(self):
        for email in self.users_to_delete:
            response = self.delete_user(email)
            assert response.status_code == 202, \
                f"Ожидался код 202, получен {response.status_code}. Ответ: {response.text}"

    def generate_random_email(self):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(8))
        return f"{random_string}@test.com"

    def generate_random_name(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(8)).capitalize()


