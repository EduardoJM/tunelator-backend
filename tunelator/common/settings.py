from pathlib import Path
import environ
import os

#
# read env
#
env = environ.Env(DEBUG=(bool, False))
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

#
# basic config
#
DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = [
    "admin.tunelator.com.br",
    "api.tunelator.com.br",
    "tunelator.com.br",
    "localhost",
    "127.0.0.1",
]
LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#
# apps
#
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # django extensions
    'polymorphic',
    'adminsortable',
    # rest
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    # background tasks
    'django_celery_results',
    'django_celery_beat',
    # custom tunelator apps
    'authentication',
    'plans',
    'payments',
    'mails',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.static',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#
# Auth
#
AUTH_USER_MODEL = 'authentication.User'
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

#
# Database
#
DATABASES = {
    'default': env.db(),
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#
# Media and Static
#
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "media").replace("\\", "/")
MEDIA_URL = "/media/"

AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_DOMAIN')
AWS_STORAGE_BUCKET_NAME = env('AWS_S3_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

#
# Celery Task Result
#
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

#
# Mercado Pago
#
MP_PUBLIC_KEY = "APP_USR-d1e7f8c6-3d75-4f58-82d2-efadbec103ae"
MP_ACCESS_TOKEN = "APP_USR-7029564028727729-040317-ca924e9519a29602294a56aea11284bf-1100657934"
MP_APPLICATION_ID = "7029564028727729"

#
# User System
#
USER_SYSTEM_URL = "https://usersystem.tunelator.com.br"
USER_SYSTEM_AUTHORIZATION = env('USER_SYSTEM_AUTHORIZATION')

#
# CORS
#
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:3000',
    'http://localhost:3000',
    'https://dashboard.tunelator.com.br',
    'https://f925-179-54-146-220.ngrok.io',
]

#
# SMTP
#
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

MP_ACCESS_TOKEN = env('MP_ACCESS_TOKEN')

STRIPE_ACCESS_TOKEN = env('STRIPE_ACCESS_TOKEN')

