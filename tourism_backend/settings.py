from google.oauth2 import service_account
from datetime import timedelta
from pathlib import Path
import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG = (bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR,'.env'))

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #PACKAGES
    'rest_framework',
    'knox',
    #APPS
    'indianrailwaysapp',
    'userapp',
    'productapp',
    'businessapp',
    'mobileapp',
    'geographyapp',
]

AUTH_USER_MODEL = 'userapp.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tourism_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': 
    ['knox.auth.TokenAuthentication',],

     'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],

    'DEFAULT_THROTTLE_RATES': {
        'anon' : '100000/day',
        'user' : '10000/day'
    }
}

REST_KNOX = {'TOKEN_TTL': None}

WSGI_APPLICATION = 'tourism_backend.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Google Cloud Storage
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, 'credential.json'))
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = env('GOOGLE_CLOUD_STORAGE_BUCKET')
MEDIA_URL = 'https://storage.googleapis.com/media/{}/'.format(GS_BUCKET_NAME)
GS_FILE_OVERWRITE = True
GS_BLOB_CHUNK_SIZE = 1024 * 256 * 40



# Read From .env
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DEBUG')

# Postgres database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_PGSQL_NAME'),
        'USER': env('DB_PGSQL_USER'),
        'PASSWORD': env('DB_PGSQL_PWD'),
        'HOST': env('DB_PGSQL_HOST'),
        'PORT': env('DB_PGSQL_PORT'),
    }
}

# Mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER_CUSTOMER_SERVICE = env('EMAIL_CUSTOMER_SERVICE_MAIL')
EMAIL_HOST_PASSWORD_CUSTOMER_SERVICE = env('EMAIL_CUSTOMER_SERVICE_PWD')
