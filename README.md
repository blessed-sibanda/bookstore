# Book Store

## Online Book Store Django Application

---

## Instructions

- download and install Python3 and PostgreSQL RDMS

- clone or download this repo

```commandline
cd <repo-name>
```

- create and activate Python3 virtual environment

```commandline
python3 -m venv venv
```

- install pip dependencies

```commandline
(venv) pip install -r requirements.txt
```

- create postgresql database in **psql** shell

```postgresql
CREATE DATABASE bookstore;
CREATE USER bookstore;
GRANT ALL ON DATABASE bookstore to "bookstore";
ALTER USER bookstore PASSWORD '1234pass';
ALTER USER bookstore CREATEDB;
```

- run database migrations

```commandline
(venv) python manage.py migrate
```

- run tests with coverage

```commandline
(venv) coverage run --branch --source=main manage.py test

(venv) coverage report
```

- create superuser

```commandline
(venv) python manage.py createsuperuser
```

- load some sample data (on unix based OS use forward slashes for the paths)

```commandline
(venv) python manage.py import_data main\fixtures\product-sample.csv main\fixtures\product-sampleimages 
```

- run the development server

```commandline
(venv) python manage.py runserver
```
