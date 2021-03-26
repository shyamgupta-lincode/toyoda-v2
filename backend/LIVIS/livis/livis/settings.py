"""
Django settings for livis project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import uuid
uuid._uuid_generate_random = None

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&bcp2m66%6+r#@j5o!^2)6ax-k=k669i@b6-rd23l8f+#c7o7$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000


CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
       'http://127.0.0.1:4200',
       'http://127.0.0.1',
       'http://localhost:4200',
)

ENCRYPT_ID = '$pbkdf2-sha256$29000$6/3/XysF4JxT6j3H.J/Tug$uGi.a8mgaM1m5ze1mCTMNu0oljqOI78ha9TyMFtekbs'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'djcelery',
    'accounts.apps.AccountsConfig',
    'parts.apps.PartsConfig',
    'shifts.apps.ShiftsConfig',
    'reports.apps.ReportsConfig',
    'capture.apps.CaptureConfig',
    'workstations.apps.WorkstationsConfig',
    'annotate.apps.AnnotateConfig',
    'plan.apps.PlanConfig',
    'toyoda.apps.ToyodaConfig',
    'training.apps.TrainingConfig',
    'logs.apps.LogsConfig',
    'assects.apps.AssectsConfig',
    'crm.apps.CrmConfig',
    'preprocess.apps.PreprocessConfig',
    'inspection.apps.InspectionConfig',
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',

]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3030',
] # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
CORS_ORIGIN_REGEX_WHITELIST = [
    'http://localhost:3030',
]

ROOT_URLCONF = 'livis.urls'

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

WSGI_APPLICATION = 'livis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'


#Setting key for Customised User Model
AUTH_USER_MODEL = 'accounts.User'

#Settings for MongoDB
MONGO_SERVER_HOST = "13.234.202.181"
MONGO_SERVER_PORT = 7778
MONGO_DB = "LIVIS"
#MONGO_DB = "TOYODA"
MONGO_COLLECTION_PARTS = "parts"
MONGO_COLLECTIONS = {MONGO_COLLECTION_PARTS: "parts"}
WORKSTATION_COLLECTION = 'workstations'
PARTS_COLLECTION = 'parts'
SHIFT_COLLECTION = 'shift'
PLAN_COLLECTION = 'plan'
LOGS_COLLECTION = 'logs'
ASSECTS_COLLECTION = 'assects'
MODEL_COLLECTION = 'model_collections'
INSPECTION_COLLECTION = 'inspection'
EXPERIMENT_COLLECTION = 'experiment'
KANBAN_COLLECTION = 'kanban_collection'
PREPROCESSING_COLLECTION = '{}_preprocessingpolicy'
LEADS_COLLECTION = 'leads'
TASKS_COLLECTION = 'tasks'
LEAD_SOURCE_COLLECTION = 'lead_source'
#Settings for Redis
REDIS_CLIENT_HOST = "localhost"
REDIS_CLIENT_PORT = 6379

CELERY_BROKER_URL = 'redis://localhost:6379'
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
CELERYD_FORCE_EXECV = True

TRAIN_DATA_STATIC = "/datadrive/image_data"
EXPERIMENT_DATA_STATIC = '/root/experiments'
print("AREEEEE: : : : :   " , TRAIN_DATA_STATIC)
if not os.path.exists(TRAIN_DATA_STATIC):
    os.makedirs(TRAIN_DATA_STATIC)

BASE_URL = '13.234.202.181'

# For Capture service
KAFKA_BROKER_URL = "13.127.161.4:9092"
consumer_mount_path = "/Livis"
mongo_host = "mongodb"
mongo_port = 27017


# List of Avalaible ports for Tensprbaords
TF_PORTS = [4200,3306,4400,3000,9092,2181,37685,33253]

