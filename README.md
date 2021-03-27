# ETL by Django Command

## **Installation:**

1.  Clone this repo

        $git clone https://github.com/DavidCastilloAlvarado/django_rssapp.git

        $cd django_rssapp

2.  Install and active the environment (power shell)

        $python -m pip install --user virtualenv
        $python -m venv .
        $source ./Scripts/activate

3.  Download all required libraries

        $pip install -r requirements.txt

## **Quickstart**

1. Set your own database credential Postgresql or just keep using SQLite

In `djangoblog/settings.py`:

```python

   'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'opencovidlocal',
        'USER': 'postgres',
        'PASSWORD': 'admin1234',
        'HOST': '127.0.0.1',
        'DATABASE_PORT': '5432',
    }
```

2.  Make all migrations before to run

```shell

        $python manage.py makemigrations
        $python manage.py migrate
```

## **Using**

### Test

```shell

$python manage.py runserver
$python manage.py test

```

### Run the server and enjoy

```shell

$python manage.py runserver
```
