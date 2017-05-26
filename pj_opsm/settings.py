import os






DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []



INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'xadmin',
    'crispy_forms',
    'apps',
    'devices',
    'record',
    'djcelery',
    'kombu.transport.django',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pj_opsm.urls'

WSGI_APPLICATION = 'pj_opsm.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pj_opsm',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'opsm',
        'PASSWORD': '11111',
    }
}



LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i'
TIME_FORMAT = 'H:i'


STATIC_URL = '/static/'


BROKER_URL = 'redis://127.0.0.1:6379/0'
BROKER_TRANSPORT = 'redis'
