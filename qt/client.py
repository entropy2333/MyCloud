import json
import requests
import hashlib


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

    def upload(self, username, filepath, pwd=''):
        with open(filepath, 'rb') as f:
            file = f.read()
        md5 = hashlib.md5(file).hexdigest()
        filename = filepath.split('/')[-1]
        filetype = filepath.split('.')[-1].lower()
        data = {
            "ua": self.UA,
            "username": username,
            "filename": filename,
            "data": file,
            "type": filetype,
            "md5": md5,
            "pwd": ''
        }
        response = self.post(f'{self.SERVER_URL}/upload_file/', data)
        response = response.json()
        if response['upload_flag']:
            return True
        else:
            return response['error_info']


if __name__ == "__main__":
    client = Client()
    print(client.user_login('mkf', '123'))
    print(client.fetch_all_file())
