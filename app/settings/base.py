# coding: utf-8

from __future__ import unicode_literals

import os

from django.core.exceptions import ImproperlyConfigured


def project_abs_path(*path):
    return os.path.join(
        os.path.normpath('{}/../../'.format(os.path.dirname(__file__))), *path
    )


def app_abs_path(*path):
    return os.path.join(
        os.path.normpath('{}/../'.format(os.path.dirname(__file__))), *path
    )


def get_env(name):
    try:
        return os.environ[name]
    except KeyError:
        raise ImproperlyConfigured(
            "Set the {} environment variable".format(name))


def _(s):
    return s

DEBUG = True

APPEND_SLASH = True

LOGIN_URL = '/user/login'
LOGIN_REDIRECT_URL = '/user/dashboard'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
)

DEFAULT_FILE_STORAGE = 'mtr.utils.storage.OverwriteDublicateFileSystemStorage'

SESSION_COOKIE_NAME = 'app'

DOMAIN_URL = 'http://somerealname.com'

CONN_MAX_AGE = 60

LANGUAGES = (
    ('ru', _('Русский')),
    ('en', _('Английский')),
)


MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_DEBUG = DEBUG

ADMINS = (
    ('Yaroslav Rudenok', 'yaroslavprogrammer@gmail.com'),
)

MANAGERS = ADMINS
SERVER_EMAIL = 'app@somerealname.com'

DATABASES = {
    'default': {
        'ENGINE': get_env('DB_ENGINE'),
        'NAME': get_env('DB_NAME'),
        'USER': get_env('DB_USER'),
        'PASSWORD': get_env('DB_PASSWORD'),
        'HOST': get_env('DB_HOST'),
        'PORT': get_env('DB_PORT'),
    },
}

TIME_ZONE = 'Europe/Kiev'
LANGUAGE_CODE = 'ru'

USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True

MEDIA_ROOT = project_abs_path('media')
MEDIA_URL = '/media/'

STATIC_ROOT = project_abs_path('static')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = get_env('SECRET_KEY')

TEMPLATES = ({
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': (app_abs_path('templates'),),
    'APP_DIRS': True,
    'OPTIONS': {
        'debug': DEBUG,
        'context_processors': (
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.request',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
        )
    }},
)

MIDDLEWARE_CLASSES = (
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'

INSTALLED_APPS = (
    'rest_framework',

    'suitlocale',
    'suit',

    'django_extensions',

    'django.contrib.postgres',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.admin',

    'app.components.sites',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '162.243.100.206'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587

CACHES = {
    "default": {
        "BACKEND": get_env('REDIS_BACKEND'),
        "LOCATION": get_env('REDIS_LOCATION'),
        "OPTIONS": {
            "CLIENT_CLASS": get_env('REDIS_OPTIONS_CLIENT_CLASS'),
            'PARSER_CLASS': get_env('REDIS_OPTIONS_PARSER_CLASS'),
        },
        'KEY_PREFIX': get_env('CACHE_PREFIX')
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'


SUIT_CONFIG = {
    'ADMIN_NAME': 'App',
    'LIST_PER_PAGE': 64,
    'HEADER_DATE_FORMAT': 'l, d, F Y',
    'SEARCH_URL': 'admin:sites_site_changelist',
    'MENU_ICONS': {
        'auth': 'icon-lock',
    },
}
