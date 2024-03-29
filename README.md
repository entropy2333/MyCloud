# Mycloud

## Preview

![](docs/img/主界面.png)
![](docs/img/qt主界面.png)

## Requirements

- Python 3.7,
- Django 3.0.3
- MySQL
- PyMySQL 0.9.3

## Run the code

### Initialize Database

```sql
mysql -u root -p
CREATE DATABASE cloud;
```

```sh
python manage.py makemigrations --empty index
python manage.py makemigrations
python manage.py migrate
```

### Modify Encode

this step is necessary to avoid encode error

```sql
use cloud;
ALTER TABLE index_fileinfo CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE index_folderinfo CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE index_shareinfo CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
```

### Start

server

```sh
python manage.py runserver 0.0.0.0:8000  
```

client

```sh
cd ./qt
python ./main.py
```
