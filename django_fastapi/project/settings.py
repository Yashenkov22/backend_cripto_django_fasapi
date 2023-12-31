import os

from config import DB_USER, DB_PASS, DB_HOST, DB_NAME, DB_PORT


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "secret-key"

DEBUG = True

LANGUAGE_CODE = 'ru'

# TIME_ZONE = 'Europe/Moscow'

# SITE_DOMAIN = 'wttonline.ru'
# SITE_DOMAIN = '127.0.0.1:8000'

# ALLOWED_HOSTS = [SITE_DOMAIN]

# CSRF_TRUSTED_ORIGINS = [f'https://{SITE_DOMAIN}']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    "django_celery_beat",
    "general_models",
    "no_cash",
    "cash",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        # "NAME": "test_api_db",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASS,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_holder'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


STATIC_URL = "/django/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PROJECT_NAME = "django-fastapi-project"

CELERY_IGNORE_RESULT = True
# CELERY_BROKER_URL='amqp://guest:guest@rabbitmq3:5672/'

FASTAPI_PREFIX = "/api"
DJANGO_PREFIX = "/django"

# DEV_PROTO = 'http://'
# PROTOCOL = 'https://'


####SWITCH FOR DEV/PROD##########

SITE_DOMAIN = 'wttonline.ru'
# SITE_DOMAIN = '127.0.0.1:8000'

ALLOWED_HOSTS = [SITE_DOMAIN]

CSRF_TRUSTED_ORIGINS = [f'https://{SITE_DOMAIN}']

CELERY_BROKER_URL='amqp://guest:guest@rabbitmq3:5672/'

PROTOCOL = 'https://'