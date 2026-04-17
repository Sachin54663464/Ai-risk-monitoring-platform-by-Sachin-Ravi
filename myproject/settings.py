"""
Django settings for myproject project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-2bibv1xcr8va4*pge6m9hr*)eew$pbr1@)cw+c8ns*es$3k1%l'

DEBUG = True

ALLOWED_HOSTS = []


# ======================================
# APPLICATIONS
# ======================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',

    # Local
    'core',
]


# ======================================
# MIDDLEWARE
# ======================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ======================================
# URL CONFIG
# ======================================

ROOT_URLCONF = 'myproject.urls'


# ======================================
# TEMPLATES
# ======================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # global templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ======================================
# WSGI
# ======================================

WSGI_APPLICATION = 'myproject.wsgi.application'


# ======================================
# DATABASE
# ======================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ======================================
# PASSWORD VALIDATION
# ======================================

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


# ======================================
# INTERNATIONALIZATION
# ======================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ======================================
# STATIC FILES
# ======================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # create this folder manually if needed
]

STATIC_ROOT = BASE_DIR / 'staticfiles'  # production use


# ======================================
# MEDIA FILES
# ======================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ======================================
# DEFAULT PRIMARY KEY
# ======================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/admin/login/'