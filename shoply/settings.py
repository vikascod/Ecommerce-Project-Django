from pathlib import Path
import dotenv
from django.utils.crypto import get_random_string
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


# SECRET_KEY = 'mo0+91hv5^(kcgl#@02!)_v@pga_nlnj!-96&@a7-no)08g3'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'mo0+91hv5^(kcgl#@02!)_v@pga_nlnj!-96&@a7-no)08g3')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = str(os.environ.get('DEBUG'))=="1"

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'seahorse-app-uge7d.ondigitalocean.app']

# if not DEBUG:
#     ALLOWED_HOSTS += [os.environ.get('DJANGO_ALLOWED_HOST')]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'app',
    'captcha',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
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

ROOT_URLCONF = 'shoply.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'shoply.wsgi.application'


if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    POSTGRES_DB = config('POSTGRES_DB')
    print(POSTGRES_DB)
    POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
    print(POSTGRES_PASSWORD)
    POSTGRES_USER = config('POSTGRES_USER')
    print(POSTGRES_USER)
    POSTGRES_HOST = config('POSTGRES_HOST')
    print(POSTGRES_HOST)
    POSTGRES_PORT = config('POSTGRES_PORT')
    print(POSTGRES_PORT)

    POSTGRES_READY = (
        POSTGRES_DB is not None
        and POSTGRES_PASSWORD is not None
        and POSTGRES_USER is not None
        and POSTGRES_HOST is not None
        and POSTGRES_PORT is not None
    )

    if POSTGRES_READY:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": POSTGRES_DB,
                "USER": POSTGRES_USER,
                "PASSWORD": POSTGRES_PASSWORD,
                "HOST": POSTGRES_HOST,
                "PORT": POSTGRES_PORT,
            }
        }




CACHE_TTL = 60

CACHES = {
    "default":{
        "BACKEND":"django_redis.cache.RedisCache",
        "LOCATION":"redis://default:UyKbsk3noBII95dpSILZ4GKhhh5kwD4k@redis-11988.c84.us-east-1-2.ec2.cloud.redislabs.com:11988",
        "OPTIONAL":{
            "CLIENT_CLASS":"django_redis.cache.DefaultClient"
        },
        "KEY_PREFIX":"exaple"
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': '5cea40b07ad25fec660e',
            'secret': '6536236ad4e567add25bffcd2ab511924c2b0fd7',
            'key': ''
        }
    },
    'google': {
        'APP': {
            'client_id': '958407627570-ue1fcpnjmac4delr2dlltqn30gfu3uc4.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email'
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = (BASE_DIR / 'static')

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
