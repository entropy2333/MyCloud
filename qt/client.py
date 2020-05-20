import json
import requests
import hashlib
import os
import base64


class Client(requests.Session):

    def __init__(self):
        super().__init__()
        self.SERVER_URL = 'http://127.0.0.1:9999'
        self.UA = 'pyqt'
        self.upload_process = {}

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
            return response['error_info']

    def fetch_all_file(self):
        params = {
            'ua': self.UA
        }
        response = self.get(f'{self.SERVER_URL}/', params=params)
        response = response.json()
        return response

    def upload(self, username, filepath, pwd=''):
        file = []
        file_all = b''
        size_all = os.path.getsize(filepath)
        size_finish = 0
        CHUNK_SIZE = 1048576
        filename = filepath.split('/')[-1]
        filetype = filepath.split('.')[-1].lower()
        with open(filepath, 'rb') as f:
            while True:
                a = f.read(CHUNK_SIZE)
                if len(a):
                    a_base64 = base64.encodebytes(a).decode("utf-8")
                    file_all += a
                    size_finish += len(a)
                    self.upload_process[filename] = size_finish / size_all
                    file.append(a_base64)
                else:
                    f.close()
                    break
        data = {
            "ua": self.UA,
            "username": username,
            "filename": filename,
            "type": filetype,
            "pwd": pwd,
            'length': len(file)
        }
        md5 = hashlib.md5(file_all).hexdigest()
        data["md5"] = md5
        # data["encoding"] = chardet.detect(file[0])['encoding']
        for index, d in enumerate(file):
            data[f'data{index}'] = d
        response = self.post(f'{self.SERVER_URL}/upload_file/', data)
        response = response.json()
        self.upload_process.pop(filename)
        if response['upload_flag']:
            return True
        else:
            return response['error_info']

    def download(self, filepath, savepath='e:\\'):
        response = self.get(
            f'{self.SERVER_URL}/download_file/?file_path={filepath}&ua=pyqt')
        response = response.json()
        length = response['length']
        md5 = response['md5']
        filename = response['filename']
        data = []
        for i in range(length):
            data.append(base64.b64decode(response[f'data{i}']))
        data_all = b''
        for i in data:
            data_all += i
        md5_ = hashlib.md5(data_all).hexdigest()
        if md5 != md5_:
            return {
                "download_flag": False,
                "error_info": "MD5 error!"
            }
        else:
            path = os.path.join(savepath, 'Downloads', filename)
            version = 0
            while os.path.exists(path):
                version += 1
                p, suffix = path.rsplit('.', 1)
                path = (p.rsplit(
                    '(', 1)[0] if version else p) + f'({version}).' + suffix
            with open(path, 'wb+') as f:
                for i in data:
                    f.write(i)
                f.close()
            return {"upload_flag": True}


if __name__ == "__main__":
    client = Client()
    print(client.user_login('ddd', '1'))
    # print(client.fetch_all_file())
    # print(client.upload('ddd', 'e:/qt测试.txt', pwd=''))
    print(client.download('ddd/qt测试.txt'))
