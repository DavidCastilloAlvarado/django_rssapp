# Rss APP by Django

## **Installation:**

1.  Clone this repo

```shell
        $git clone https://github.com/DavidCastilloAlvarado/django_rssapp.git
        $cd django_rssapp
```

2.  Install and active the environment (power shell)

```shell
        $python -m pip install --user virtualenv
        $python -m venv .
        $source ./Scripts/activate
```

3.  Download all required libraries

```shell
        $pip install -r requirements.txt
```

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
        $cd djangoblog
        $python manage.py makemigrations
        $python manage.py migrate
```

## **Using**

### Test all, models, serializers, functions

```shell

        $python manage.py test

```

### Run the server and enjoy

```shell

        $python manage.py runserver

```

## **Resume**

This works using the sqlite database

```shell
git clone https://github.com/DavidCastilloAlvarado/django_rssapp.git
cd django_rssapp
python -m pip install --user virtualenv
python -m venv .
source ./Scripts/activate
cd djangoblog
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py runserver
```

## **Templates**

### 1. Home page

<center>
<img src="img/home.PNG" alt="drawing" width="600"/>
</center>

### 1.1. Login page

<center>
<img src="img/login.PNG" alt="drawing" width="600"/>
</center>

### 1.2. Signup page

<center>
<img src="img/signup.PNG" alt="drawing" width="600"/>
</center>

### 2. Home User page

<center>
<img src="img/homeuser.PNG" alt="drawing" width="600"/>
</center>

### 3. Add a new feed

<center>
<img src="img/createfeed.PNG" alt="drawing" width="600"/>
</center>
