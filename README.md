# Mycloud

## Requirements

- Python 3.7,
- Django 3.0.3
- MySQL
- PyMySQL 0.9.3

## Run the code

### Initialize Database

```sql
mysql -uroot -p
CREATE DATABASE cloud;
```

```sh
python manage.py makemigrations  
python manage.py migrate  
```

### Modify Encode

this step is necessary to avoid encode error

```sql
use cloud;
ALTER TABLE index_fileinfo CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
ALTER TABLE index_folderinfo CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
```

### Start Server

```sh
python manage.py runserver 0.0.0.0:8000  
```