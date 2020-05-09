import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'campusbuy',
        'USER': 'maro',
        'PASSWORD': 'guido van rossum',
        'HOST': 'localhost',
        'PORT': '',
    }
}

DEBUG = True

