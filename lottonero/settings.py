from pathlib import Path
import os
import dj_database_url
if os.path.isfile('env.py'):
    import env


# Use the DATABASE_URL environment variable for database configuration
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# Set DEBUG based on the 'DEVELOPMENT' environment variable
DEBUG = os.environ.get("DEVELOPMENT") == "True"

# You can also print the DEBUG status for verification
print(f"DEBUG is set to: {DEBUG}")

# CORS settings
CORS_ALLOWED_ORIGINS = [
    'https://8000-jjsemaan-lottonero-pykwwkf1hp.us1.codeanyapp.com',
    'https://lottonero-e7dc9a7038d2.herokuapp.com',
    'https://*.codeanyapp.com',
    'https://*.codeinstitute-ide.net',
    'https://*.gitpod.io',
    'https://*.herokuapp.com',
    'https://*.lottonero.com',
]

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    'https://8000-jjsemaan-lottonero-pykwwkf1hp.us1.codeanyapp.com',
    'https://lottonero-e7dc9a7038d2.herokuapp.com',
    'https://*.codeanyapp.com',
    'https://*.codeinstitute-ide.net',
    'https://*.gitpod.io',
    'https://*.herokuapp.com',
    'https://*.lottonero.com',
]

# Allowed hosts
ALLOWED_HOSTS = [
    '8000-jjsemaan-lottonero-3e6m081kr94.ws.codeinstitute-ide.net',
    '8000-jjsemaan-lottonero-pykwwkf1hp.us1.codeanyapp.com',
    'lottonero-e7dc9a7038d2.herokuapp.com',
    'https://*.codeanyapp.com',
    'https://*.codeinstitute-ide.net',
    'https://*.gitpod.io',
    'https://*.herokuapp.com',
    'https://*.lottonero.com',
    'localhost', '127.0.0.1', 'da99-18-202-164-254.ngrok-free.app',
]

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'tinymce',
    'cloudinary',
    'contact',
    'crispy_forms',
    'crispy_bootstrap4',
    'djstripe',
    'home',
    'scraping',
    'predictions',
    'lottery_stats',
    'corsheaders',
    'orders',
    'user_profile',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'lottonero.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
             'builtins': [
                'crispy_forms.templatetags.crispy_forms_tags',
                'crispy_forms.templatetags.crispy_forms_field',
            ]
        },
    },
]

# CRISPY FORMS SETTINGS
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Configure authentication backends
AUTHENTICATION_BACKENDS = [
    # Needed to authenticate via username/password
    'django.contrib.auth.backends.ModelBackend',
    # Django-allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_FORMS = {
    'signup': 'lottonero.forms.CustomSignupForm', 
}

# Set up your site ID
SITE_ID = 1

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587  # Use 465 for SSL or 587 for TLS
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

WSGI_APPLICATION = 'lottonero.wsgi.application'

# Example configurations for Google and Facebook
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'YOUR_GOOGLE_CLIENT_ID',
            'secret': 'YOUR_GOOGLE_CLIENT_SECRET',
            'key': ''
        }
    },
    'facebook': {
        'APP': {
            'client_id': 'YOUR_FACEBOOK_APP_ID',
            'secret': 'YOUR_FACEBOOK_APP_SECRET',
            'key': ''
        }
    },
    # Add configurations for other providers here as needed
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# DJ-Stripe Configuration
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
DJSTRIPE_WEBHOOK_SECRET = os.environ.get('DJSTRIPE_WEBHOOK_SECRET')
DJSTRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
# DJSTRIPE_WEBHOOK_VALIDATION = 'verify_signature'

# Stripe Payment Configuration  
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_TEST_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') 
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_ENDPOINT_SECRET = os.environ.get('STRIPE_ENDPOINT_SECRET')
STRIPE_PRICING_TABLE_ID = os.environ.get('STRIPE_PRICING_TABLE_ID')
STRIPE_LIVE_MODE = False  # Change to True in production


# Cloudinary configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
os.makedirs(STATIC_ROOT, exist_ok=True)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_title": "Lottonero",
    "site_header": "Lottonero Admin",
    "site_brand": "Lottonero",
    "user_avatar": None,
    "welcome_sign": "Welcome Lottonero's Admin Portal!",

    # Copyright on the footer
    "copyright": "ParaBIM Ltd.",

    # Side menu
    "navigation_expanded": False,

    "usermenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Lottonero Home",  "url": "/", "permissions": ["auth.view_user"]},
    

        # external url that opens in a new window (Permissions can be added)
        {"name": "Lottonero Github Repo", "url": "https://github.com/jjsemaan/lottonero", "new_window": True},

    ],
}