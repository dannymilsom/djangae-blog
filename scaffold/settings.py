"""
Django settings for scaffold project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from djangae.settings_base import * #Set up some AppEngine specific stuff

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

from .boot import get_app_config
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_app_config().secret_key

AUTH_USER_MODEL = 'djangae.GaeDatastoreUser'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangosecure',
    'csp',
    'djangae.contrib.gauth',
    'djangae', # Djangae should be after Django core/contrib things
    'blog',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'djangae.contrib.security.middleware.AppEngineSecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'djangae.contrib.gauth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.csrf"
)

def check_session_csrf_enabled():
    if "session_csrf.CsrfMiddleware" not in MIDDLEWARE_CLASSES:
        return [ "SESSION_CSRF_DISABLED"]

    return []
check_session_csrf_enabled.messages = { "SESSION_CSRF_DISABLED" : "Please add 'session_csrf.CsrfMiddleware' to MIDDLEWARE_CLASSES" }

SECURE_CHECKS = [
    "djangosecure.check.sessions.check_session_cookie_secure",
    "djangosecure.check.sessions.check_session_cookie_httponly",
    "djangosecure.check.djangosecure.check_security_middleware",
    "djangosecure.check.djangosecure.check_sts",
    "djangosecure.check.djangosecure.check_frame_deny",
    "djangosecure.check.djangosecure.check_ssl_redirect",
    "scaffold.settings.check_session_csrf_enabled"
]

AUTHENTICATION_BACKENDS = (
    'djangae.contrib.gauth.backends.AppEngineUserAPI',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'scaffold.urls'

WSGI_APPLICATION = 'scaffold.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'djangae.db.backends.appengine'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATETIME_FORMAT = 'j F Y'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR + '/templates'),
)

if DEBUG:
    CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
# in a real production project we wouldn't do this - but to speed up dev
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com",
                "https://maxcdn.bootstrapcdn.com")
CSP_FONT_SRC = ("'self'", "'unsafe-inline'", "https://fonts.gstatic.com",
                "https://maxcdn.bootstrapcdn.com")
CSP_IMG_SRC = ("*",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-eval'")

from djangae.contrib.gauth.settings import *

LOGIN_URL = '/login'
