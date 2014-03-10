"""
Django settings for saas project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from secret_settings import *
from local_settings import *
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEV_ENV

TEMPLATE_DEBUG = DEV_ENV

ALLOWED_HOSTS = []

#in test environment database settings are different
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    TEST = True
else:
    TEST = False

if DEV_ENV:
    DB_NAME = DEVELOPMENT_DB_NAME
    DB_USERNAME = DEVELOPMENT_DB_USERNAME
    DB_PASSWORD = DEVELOPMENT_DB_PASSWORD
else:
    DB_NAME = PRODUCTION_DB_NAME
    DB_USERNAME = PRODUCTION_DB_USERNAME
    DB_PASSWORD = PRODUCTION_DB_PASSWORD

if TEST:
    DB_NAME = TEST_DB_NAME
    DB_USERNAME = TEST_DB_USERNAME
    DB_PASSWORD = TEST_DB_PASSWORD


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'centipair.core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'centipair.core.middleware.SiteMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'saas.urls'

WSGI_APPLICATION = 'saas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
#TODO: use connection pooling for database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USERNAME,
        'PASSWORD': DB_PASSWORD,
        'HOST': '',
        'PORT': '',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('en-gb', 'English Britain'),
    ('en-us', 'English United States'),
    ('fr', 'French'),
    ('de', 'German'),
)
LOCALE_PATHS = (BASE_DIR + "/locale/",)


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = 'http://localhost:8090/saas/resources/'
TEMPLATE_STATIC_URL = STATIC_URL + 'templates'
#STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/saas/resources'
UPLOAD_PATH = STATIC_ROOT + '/uploads'

USER_TEMPLATE_PATH = STATIC_ROOT + '/user-templates'
USER_FILES_PATH = BASE_DIR + '/saas/user-files'
CORE_TEMPLATE_PATH = 'centipair/core'
TEMPLATE_PATH = '/templates/'

TEMPLATE_DIRS = (
    STATIC_ROOT + '/templates',
)

APPS = {'CORE': 'core',
        'CMS': 'cms',
        'STORE': 'store',
        'BLOG': 'blog',
        'SUPPORT': 'support'}

DEFAULT_APP = APPS['CORE']
