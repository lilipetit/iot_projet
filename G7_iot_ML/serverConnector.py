import requests
import config as config

class ServerConnector():
    endpoint = config.ENDPOINT
    token = None

    def auth(self, email: str, password: str):
        payload = {"username": email.encode(), "password": password.encode()}
        response = requests.request("POST", f"{self.endpoint}/token", data=payload)
        data = response.json()
        if response.status_code == 200:
            token = f"{data['token_type']} {data['access_token']}"
            return token
        else:
            raise Exception("Authentication failed")

    def get_me(self):
        headers = {
            "Authorization": self.token,
        }
        response = requests.request("GET", f"{self.endpoint}/users/me", headers=headers)
        me = response.json()
        return me

    def mark_user_as_cheater(self, user_id, is_cheater):
        headers = {
            "Authorization": self.token,
        }
        payload = {"is_cheater": is_cheater}
        print(payload)
        response = requests.request("POST", f"{self.endpoint}/user/update/{user_id}", headers=headers, json=payload)
        print(response.text)
        return response.status_code
