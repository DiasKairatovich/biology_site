from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-test-key'  # для диплома можно так
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'localhost.localdomain']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'users',
    'tests',
    'theory',
    "ckeditor",
    "ckeditor_uploader", # для Онлайн редактора
    "rest_framework", # для DRF
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # для переключателя языка
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bioedu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'main' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'bioedu.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bioedu_db',
        'USER': 'dias',
        'PASSWORD': 'DunkBall17!',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = []

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = "ru"  # язык по умолчанию
LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
    ('kk', _('Kazakh')),
]
LOCALE_PATHS = [
    BASE_DIR / "locale",  # сюда будут сохраняться переводы
]

TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'

STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
STATIC_ROOT = BASE_DIR / "staticfiles"     # сюда collectstatic соберёт всё

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_ALLOW_NONIMAGE_FILES = True

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Full",    # Полный тулбар
        "height": 400,
        "width": "100%",
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

