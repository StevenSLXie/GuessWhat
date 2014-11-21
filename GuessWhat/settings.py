"""
Django settings for GuessWhat project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from __future__ import absolute_import

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
os.path.join(BASE_DIR,'Guess/algorithm')
os.path.join(BASE_DIR,'Guess/templatetags')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=cx=bkx2=-d1ht0=hy-lus+4u!#9($x5*r0=9#798%r+h@-=#u'

# SECURITY WARNING: don't run with debug turned on in production!
import socket
if socket.gethostname() == 'XINGs-MacBook-Pro.local':
	DEBUG = True
else:
	DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'Guess',
	'bootstrap3',
	'Guess.templatetags',
	'south',
	'djcelery',
	'redis',
	'notifications'
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'GuessWhat.urls'

WSGI_APPLICATION = 'GuessWhat.wsgi.application'


import djcelery
from celery.schedules import crontab
from datetime import timedelta
djcelery.setup_loader()

BROKER_URL = 'redis://localhost:6379/0'



CELERYBEAT_SCHEDULE = 'djcelery.schedulers.DatabaseScheduler'

CELERY_TIMEZONE = 'Asia/Shanghai'



# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

if socket.gethostname() is not 'XINGs-MacBook-Pro.local':
	STATIC_ROOT = '/opt/myenv/static/'
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
	os.path.join(BASE_DIR,  'templates'),
	os.path.join(BASE_DIR, 'Guess/templates'),
)

# Email stuff

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'stevenslxie@gmail.com'
EMAIL_HOST_PASSWORD = '2xiexing'
EMAIL_USE_TLS   = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'