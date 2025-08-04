from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# config = Config()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY",default='')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "daphne",
    "corsheaders",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "drf_yasg",
    "djoser",
    "rest_framework",
    "rest_framework_simplejwt",
    "accounts",
    "category",
    "ecommerce",
    "tag",
    "posts",
    "newsletter",
    "oauth2_provider",
    "social_django",
    "drf_social_oauth2",
]

SITE_ID = 1

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "blogs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

# WSGI_APPLICATION = 'blogs.wsgi.application'
ASGI_APPLICATION = "blogs.asgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# NEWLY ADDED SETTINGS #

# Will use accounts.CustomUser for the Authentication.
AUTH_USER_MODEL = "accounts.CustomUser"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",  # django-oauth-toolkit >= 1.0.0
        "drf_social_oauth2.authentication.SocialAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,  # Number of objects per page
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

SWAGGER_SETTINGS = {"SECURITY_DEFINITIONS": {"Basic": {"type": "basic"}}}

DJOSER = {
    # ** TO Change Domain of Activtion and Reset Password Links:
    # ** Run the following commands in Python Shell ($ python manage.py shell)
    # >>> from django.contrib.sites.models import Site
    # >>> Site.objects.update_or_create(pk=1, defaults={'domain': '127.0.0.1:3000', 'name': 'localhost'})
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "reset-password/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "reset-email/{uid}/{token}",
    "PERMISSIONS": {
        "activation": ["rest_framework.permissions.AllowAny"],
    },
    "SOCIAL_AUTH_TOKEN_STRATEGY": "djoser.social.token.jwt.TokenStrategy",
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": [
        "http://127.0.0.1:8000/facebook/",
        "http://localhost:3000/login-register",
        "http://127.0.0.1:3000/login-register",
    ],
}

# # Email Configuration

EMAIL_BACKEND=os.getenv("EMAIL_BACKEND", default="")
EMAIL_HOST = os.getenv("EMAIL_HOST", default="")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", default=0))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = bool(os.getenv("EMAIL_USE_TLS", default=""))

# EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST='sandbox.smtp.mailtrap.io'
# EMAIL_PORT=2525
# EMAIL_HOST_USER='11ffa5b86660f3'
# EMAIL_HOST_PASSWORD='9d3e6aa29c6fd5'
# EMAIL_USE_TLS=True

# Stripe Keys
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", default="")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", default="")

# To allow all origins
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = ["Authorization", "Content-Type", "Accept"]
CORS_ALLOW_CREDENTIALS = True
# SESSION_COOKIE_DOMAIN = "localhost"

# Media Uploads Settings
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# WebSockets / Channel Config
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

AUTHENTICATION_BACKENDS = (
    "drf_social_oauth2.backends.DjangoOAuth2",
    "django.contrib.auth.backends.ModelBackend",
    # Facebook Auth
    "social_core.backends.facebook.FacebookAppOAuth2",
    "social_core.backends.facebook.FacebookOAuth2",
    # Google Auth
    "social_core.backends.google.GoogleOAuth2",
)

# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("SOCIAL_AUTH_FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("SOCIAL_AUTH_FACEBOOK_SECRET")
SOCIAL_AUTH_FACEBOOK_SCOPE = ["email"]
# * Issue: Unable to get email while user creation. Add the following lines:
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {"fields": "id, name, email"}
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_USER_FIELDS = ["email", "first_name", "username", "password"]


# Google Configuration
# ! IMPORTANT !

# * ---------------- Instruction 1 ---------------- *
# ! 1. Login issue with Google Social Login:
# * Front-end needs to be hosted at the same domain.
# *     - If back-end -> 127.0.0.1 then front-end should be at -> 127.0.0.1 NOT localhost
# ! Issue: https://stackoverflow.com/questions/66205017/django-djoser-social-auth-state-could-not-be-found-in-server-side-session-dat
# * Solution: https://stackoverflow.com/questions/57305141/react-django-rest-framework-session-is-not-persisting-working/57316231#57316231

# * ---------------- Instruction 1 ---------------- *

# * ---------------- Instruction 2 ---------------- *

# ! 2. Getting Google profile picture from Google.
# ! This can be done via over-riding as well. Tried but failed :(
# * To get the User Profile Picture from Google:

# * 1. Name / Rename the Picture Field in User / Account models -> 'picture'. It is important that name of the image field is 'picture' to automatically save the profile picture.

# * 2. Go to the following file:
# *     >>> env -> lib -> python3.xx -> site-packages -> social_core -> backends -> google.py

# * 3. Go to the following method:
# *     class BaseGoogleAuth -> def get_user_details()

# * 4. Add the following lines of code:
#  >>> ... (other code)
#  >>> picture = response.get("picture", "")
#  >>> ... (other code)
#  >>> return {
#       ... (other objects to return)
#       "picture": picture,
#       ... (other objects to return)
#    }

# * Now the profile picture will be automatically set when user Sign-up/log-in.

# * ---------------- Instruction 2 ---------------- *


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ["first_name", "last_name", "picture"]
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = (
    "http://localhost:8000/auth/complete/google-oauth2/"
)

SOCIAL_AUTH_UPDATE_USER_DETAILS_ON_LOGIN = (
    True  # * Will update user details on every social login
)


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  # Storing at DB1
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
