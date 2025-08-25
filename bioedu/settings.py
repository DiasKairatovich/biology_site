from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-test-key'  # для диплома можно так
DEBUG = True
ALLOWED_HOSTS = []

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
    "django_ckeditor_5", # для редактирования окна теория
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
STATICFILES_DIRS = [BASE_DIR / 'main' / 'static']
STATIC_ROOT = BASE_DIR / "staticfiles"     # сюда collectstatic соберёт всё

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
CKEDITOR_UPLOAD_PATH = "ckeditor_uploads/"

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'underline', 'strikethrough', 'code', '|',
            'link', 'blockQuote', 'insertTable', 'mediaEmbed', 'codeBlock', '|',
            'bulletedList', 'numberedList', 'todoList', '|',
            'outdent', 'indent', '|',
            'alignment', '|',
            'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', '|',
            'highlight', 'horizontalLine', 'specialCharacters', '|',
            'undo', 'redo', '|',
            'uploadImage'
        ],
        'image': {
            'toolbar': [
                'imageTextAlternative', 'imageStyle:full', 'imageStyle:side'
            ]
        },
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells'
            ]
        },
        'height': 400,
        'width': '100%',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

