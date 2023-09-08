"""
Django settings for nekosauce project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

import os
import secrets

import dotenv

from nekosauce import utils

dotenv.load_dotenv(".env.dev")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = utils.getsecret(
    "BACKEND_SECRET_KEY", secrets.token_hex(25)
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("BACKEND_DEBUG", "False") == "True"
VERSION = "0.2"

ALLOWED_HOSTS = os.getenv("BACKEND_ALLOWED_HOSTS", "127.0.0.1 localhost").split(" ")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "rest_framework",
    "debug_toolbar",
    "django_dramatiq",
    "django_bunny",
    "nekosauce.sauces.apps.SaucesConfig",
    "nekosauce.users.apps.UsersConfig",
    "nekosauce.stats.apps.StatsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "nekosauce.middleware.DisableCSRFMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

CSRF_TRUSTED_ORIGINS = os.getenv(
    "BACKEND_CSRF_TRUSTED_ORIGINS", "http://127.0.0.1 http://localhost"
).split(" ")
CSRF_COOKIE_SECURE = True

ROOT_URLCONF = "nekosauce.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "nekosauce.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME", "nekosauce"),
        "USER": os.getenv("DATABASE_USERNAME", "nekosauce"),
        "PASSWORD": utils.getsecret("DATABASE_PASSWORD", "nekosauce"),
        "HOST": os.getenv("DATABASE_HOSTNAME", "database"),
        "PORT": os.getenv("DATABASE_PORT", "5432"),
    }
}

AUTH_USER_MODEL = "users.User"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FileUploadParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "nekosauce.authentication.ApiKeyAuthentication",
    ],
    "EXCEPTION_HANDLER": "nekosauce.exceptions.exception_handler",
}


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: request.user.is_authenticated
    & request.user.is_superuser,
}


DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.rabbitmq.RabbitmqBroker",
    "OPTIONS": {
        "url": f"amqp://{os.getenv('RABBITMQ_USERNAME', 'guest')}:{os.getenv('RABBITMQ_PASSWORD', 'guest')}@{os.getenv('RABBITMQ_HOSTNAME', 'localhost')}:{os.getenv('RABBITMQ_PORT', '5672')}",
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
        "django_dramatiq.middleware.AdminMiddleware",
    ],
}
DRAMATIQ_AUTODISCOVER_MODULES = ["tasks"]

BUNNY_USERNAME = os.getenv("BACKEND_BUNNY_USERNAME", "")
BUNNY_PASSWORD = os.getenv("BACKEND_BUNNY_PASSWORD", "")
BUNNY_HOSTNAME = os.getenv("BACKEND_BUNNY_HOSTNAME", "")
BUNNY_REGION = os.getenv("BACKEND_BUNNY_REGION", "de")

STORAGES = {
    "default": {
        "BACKEND": "django_bunny.storage.BunnyStorage",
        "OPTIONS": {"base_dir": ""},
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
