from .base import *

DEBUG = False
MODELTRANSLATION_DEBUG = DEBUG

TEMPLATES = ({
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': (app_abs_path('templates'),),
    'OPTIONS': {
        'debug': DEBUG,
        'context_processors': (
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.request',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
        ),
        'loaders': (
            ('django.template.loaders.cached.Loader', (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            )),
        ),
    }},
)

# CHANGE: to real ips
ALLOWED_HOSTS = ('*',)
