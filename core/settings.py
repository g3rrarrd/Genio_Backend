import environ
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    
    'rest_framework',
    'apps.categoria',
    'apps.usuario',
    'apps.pregunta',
    'apps.ronda',
]

CORS_ALLOW_ALL_ORIGINS = True
ALLOWED_HOSTS = ['https://geniobackend-faawf6f0hbewfdbj.centralus-01.azurewebsites.net', 'geniobackend-faawf6f0hbewfdbj.centralus-01.azurewebsites.net']

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

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # E410
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # E408
    'django.contrib.messages.middleware.MessageMiddleware', # E409
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

IF_AZURE = os.path.exists('/home/site')

if IF_AZURE:
    if not os.path.exists('/home/data'):
        os.makedirs('/home/data', exist_ok=True)
    
    DB_PATH = '/home/data/db.sqlite3'
else:
    # Desarrollo local
    DB_PATH = BASE_DIR / 'db.sqlite3'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_PATH,
    }
}

STATIC_URL = 'static/'

STATICFILES_DIRS = []

import os
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Interactivo con entra id
# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',
#         'NAME': env('DB_NAME'),
#         'USER': 'g_rodriguez@outlook.com', # <--- Tu correo real de Azure/Outlook
#         'HOST': env('DB_HOST'),
#         'PORT': '1433',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 18 for SQL Server',
#             'extra_params': (
#                 'Authentication=ActiveDirectoryInteractive;' # <--- ESTO ES LA CLAVE
#                 'Encrypt=yes;'
#                 'TrustServerCertificate=no;'
#                 'Connection Timeout=30;'
#             ),
#         },
#     }
# }
