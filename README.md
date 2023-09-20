## Main Files: Project Structure

```shell
C:.
│   .env
│   manage.py
│   README.md
│
├───authentications
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   serializer.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   └───__init__.py
│
├───exceptions
│   │   exceptions.py
│   └───__init__.py
├───group
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   serializer.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   └───__init__.py
│
├───media
│   ├───images
│   └───videos
├───post
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   serializer.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
├───profiles
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   serializer.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   └───__init__.py
├───socialApp
│   │   asgi.py
│   │   urls.py
│   │   wsgi.py
│   │   __init__.py
│   │
│   ├───settings
│   │   │   base.py
│   │   │   development.py
│   │   │   production.py
│   │   └───   __init__.py
│
└───utils
    │   email_service.py
    └───__init__.py
```

## Installation steps

1. Ensure you have python3 installed
2. Clone the repository
3. create a virtual environment using `virtualenv venv`
4. Activate the virtual environment by running `source venv/bin/activate`

* On Windows use `source venv\Scripts\activate`

5. Install the dependencies using `pip install -r requirements.txt`
6. Migrate existing db tables by running `python manage.py migrate`
7. Run the django development server using `python manage.py runserver`
8. Run Celery worker using `celery -A socialApp worker -l INFO -P gevent` on another proccess.
