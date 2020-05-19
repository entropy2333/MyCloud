import json

import requests
from django.template.context_processors import csrf


SERVER_URL = 'http://127.0.0.1:9999'

    
def user_login(username, password):
    data = {
        'username': username,
        'password': password,
        'ua': 'pyqt'
    }
    r = requests.post(f'{SERVER_URL}/login/?next=/', data)
    r = r.json()
    if r['login_flag']:
        return True
    else:
        return False

def user_register(username, password, repassowrd):
    data = {
        'username': username,
        'password': password,
        'repassword': repassowrd,
        'ua': 'pyqt'
    }
    r = requests.post(f'{SERVER_URL}/register/')
    r = r.json()
    if r['register_flag']:
        return True
    else:
        return r['error_info']
    

if __name__ == "__main__":
    print(user_login('mkf', '123'))
    print(user_login('mkf', '1234'))
    print('123')