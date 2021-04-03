"""
Django settings for web_project project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os # new
from pathlib import Path
from django.conf.global_settings import MEDIA_ROOT, MEDIA_URL

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
MEDIA_DIR = os.path.join(BASE_DIR, "media")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dhh_+es(!dq91dn&_pv+ofj83t(rpj2xdnrcfk%n6hjduv@z2!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['mazen15.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web_app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'web_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

LOGGING = {
    'version':1,
    'disable_existing_loggers': False,
    'filters':{
        'require_debug_false':{
            '()': 'django.utils.log.RequireDebugFalse'}
            },
        'formatters':{
            'simple':{
                'format': '%(module)s line: %(lineno)s: %(message)s'},
            'level_app':{
                'format': '%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s| %(message)s'
                }
            },
        
        'handlers':{
            'console':{
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'level_app'
                },
            'main_log_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': '%s/main.log' %(BASE_DIR),
                'formatter': 'level_app'
                }
            },
        
        'loggers':{
            'django': {
                'handlers': ['console', 'main_log_file'],
                'level': 'ERROR',
                'propagate': True
                },
            'requests': {
                'handlers': ['console', 'main_log_file'],
                'level': 'INFO',
                'propagate': True,
                },
            '':{'handlers': ['console', 'main_log_file'],
                'level': 'DEBUG',
                'propagate': True,
                }}
        }
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'