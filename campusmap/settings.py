import os
import pkg_resources

PROJECT_NAME = 'campusmap'

DOMAIN_NAME = 'campusmap.stage.rc.pdx.edu'

BASE_DIR = os.path.dirname(pkg_resources.resource_filename(PROJECT_NAME, ''))

SECRET_KEY = 'not secret'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'arcutils',
    'campusmap.map',
]

MIDDLEWARE_CLASSES = []

ROOT_URLCONF = '{PROJECT_NAME}.urls'.format(**locals())

WSGI_APPLICATION = 'campusmap.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

STATICFILES_DIRS = (
    pkg_resources.resource_filename(PROJECT_NAME, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    pkg_resources.resource_filename(PROJECT_NAME, 'templates'),
)
