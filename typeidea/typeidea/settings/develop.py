from .base import * #NOQA


DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER': 'root',
        'PASSWORD': 'taorui',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# INSTALLED_APPS += [
#     'debug_toolbar',
# ]
#
# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ]

INTERNAL_IPS = ['127.0.0.1']