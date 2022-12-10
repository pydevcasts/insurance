

import os, socket
from pathlib import Path
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-rx8bm1hi_^n!_a_5&bjkx0p0du$x(a6ws7_46sk$zx@j8z7w+6"

DEBUG = os.environ.get("DEBUG")

ALLOWED_HOSTS = ['academybime.com', 'www.academybime.com', '*']
CSRF_TRUSTED_ORIGINS = ['academybime.com','www.academybime.com', 'https://*.academybime.com', 'http://*.academybime.com', '*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'api.apps.ApiConfig',
    'category.apps.CategoryConfig',
    'django.contrib.sites',
    'tag.apps.TagConfig',
    'contact',
    'dashboard.apps.DashboardConfig',
    'accounts.apps.AccountsConfig',
    'rest_framework',
    'widget_tweaks',
    'social_django',
    'users', 
    'debug_toolbar',
    'ckeditor',
    'django.contrib.sitemaps',
    'rest_framework.authtoken',
    'dj_rest_auth',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', # for Google OAuth 2.0

    'dj_rest_auth.registration',
    'django_filters',
    'search.apps.SearchConfig',
    'aboutus',
    'team',
    'slider',
    'faq',
    'newsletters',
    'renewal',
    'news',
    'feedback',
    'comment',
    'tickets',
    'star_ratings',
    'captcha',


    ]



ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'insurance.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'settings.context_processors.context_processors.posts_view_context_processor',
             
            ],
        },
    },
]

WSGI_APPLICATION = 'insurance.wsgi.application'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'api.permissions.IsStaffOrReadOnly',
    ],
      'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

SITE_ID = 1
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'access'
JWT_AUTH_REFRESH_COOKIE = 'refresh'

REST_AUTH_REGISTER_SERIALIZERS = {
        'REGISTER_SERIALIZER': 'api.serializers.RegisterSerializer',
}



DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':  os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    },
}

AUTH_USER_MODEL = 'accounts.User'


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


LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_I18N = True
USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media', 'upload')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'media', 'static'),
)


EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT =os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")



#Django’s Debug Toolbar Showing Inside Docker
INTERNAL_IPS = [
    "127.0.0.1",
    'localhost',
]
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]
DEBUG_TOOLBAR_CONFIG = {
    'RESULTS_CACHE_SIZE': 3,
    'SHOW_COLLAPSED': True,
    'SQL_WARNING_THRESHOLD': 100,   # milliseconds
}



CACHES = {
   'default': {
      'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
      'LOCATION': 'my_cache_table',
   }
}

RECAPTCHA_PUBLIC_KEY = "6LfVB0gjAAAAAMPIfmPJt8xSk316ITeWuZPJEAx8"
RECAPTCHA_PRIVATE_KEY = "6LfVB0gjAAAAAAKRgQDWBiceaSfjGKBq4hQjUd4U"

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '549418161873-vunmslj02haoovb8r9imscaoa2kad4sc.apps.googleusercontent.com' # Google Consumer Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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' # Google Consumer Secret
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '549418161873-mskr5f6kbobrog7lphvfu23tabbtjr88.apps.googleusercontent.com' # Google Consumer Key
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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' # Google Consumer Secret


LOGIN_REDIRECT_URL = "blog:post_and_category"  
LOGOUT_REDIRECT_URL = 'login'



# CELERY STUFF
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND'),
CELERY_ACCEPT_CONTENT = os.environ.get('CELERY_ACCEPT_CONTENT'),
CELERY_TASK_SERIALIZER = os.environ.get('CELERY_TASK_SERIALIZER'),
CELERY_RESULT_SERIALIZER = os.environ.get('CELERY_RESULT_SERIALIZER'),
CELERY_TIMEZONE = os.environ.get('CELERY_TIMEZONE')


GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')



MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-error',
 }

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

# RATINGS
STAR_RATINGS_STAR_WIDTH = 15
STAR_RATINGS_STAR_HEIGHT = 15
# # editable =
STAR_RATINGS_RERATE = False
STAR_RATINGS_ANONYMOUS = True