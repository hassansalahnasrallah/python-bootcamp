"""
Django settings for final_project project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

try:
    from final_project.local_settings import lsettings
except ImportError:
    lsettings = {}


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR,'templates')

STATIC_URL = lsettings.get('STATIC_URL', '/static/')
MEDIA_URL = lsettings.get('MEDIA_URL', '/media/')

MEDIA_ROOT = lsettings.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))
STATIC_ROOT = lsettings.get('STATIC_ROOT', os.path.join(BASE_DIR, 'final_app', 'static'))

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wq40gk%&gv3v+9hd)(%l+$in8bjj4y!6_mqwffiqw(@+lxfbox'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = lsettings.get('DEBUG', False)

ALLOWED_HOSTS = lsettings.get('ALLOWED_HOSTS', []);

LOGIN_URL = '/user_login'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'final_app',
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

ROOT_URLCONF = 'final_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'final_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#    'default': { 
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'final_project',
#        'USER':'root',
#        'PASSWORD': 'dalia',
#        'HOST':'localhost',
#        'PORT':'3306',
#         
#    }
# }

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


#LOGGING Configurations

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(module)s line: %(lineno)s: %(message)s'
        },
        'level_app':{
            'format': '%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s'
        }
        
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'level_app'
        },
        'main_log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '%s/main.log' % (BASE_DIR),
            'formatter': 'level_app'
        }
        
    },
    'loggers': {
        'django': {
            'handlers': ['console'],#, 'main_log_file'],
            'level': 'ERROR',
            'propagate': True
        },
        'requests': {
            'handlers': ['console'],#, 'main_log_file'],
            'level': 'INFO',
            'propagate': True,
        },
        '': {
            'handlers': ['console'],#, 'main_log_file'],
            'level': 'DEBUG',
            'propagate': True,
        }
        
    }
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

