import json
import requests

class Client(requests.Session):

    def __init__(self):
        super().__init__()
        self.SERVER_URL = 'http://127.0.0.1:9999'
        self.UA = 'pyqt'

    def user_login(self, username, password):
        data = {
            'username': username,
            'password': password,
            'ua': self.UA
        }
        response = self.post(f'{self.SERVER_URL}/login/?next=/', data)
        response = response.json()
        if response['login_flag']:
            return True
        else:
            return False


    def user_register(self, username, password, repassowrd):
        data = {
            'username': username,
            'password': password,
            'repassword': repassowrd,
            'ua': self.UA
        }
        response = self.post(f'{self.SERVER_URL}/login/?next=/', data)
        response = response.json()
        if response['register_flag']:
            return True
        else:
            return r['error_info']
        

    def fetch_all_file(self):
        params = {
            'ua': self.UA
        }
        response = self.get(f'{self.SERVER_URL}/', params=params)
        response = response.json()
        return response

if __name__ == "__main__":
    client = Client()
    print(client.user_login('mkf', '123'))
    print(client.fetch_all_file())