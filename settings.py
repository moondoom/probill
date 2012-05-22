# Django settings for probill project.
import django



DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'probill',                      # Or path to database file if using sqlite3.
        'USER': 'probill',                      # Not used with sqlite3.
        'PASSWORD': 'probill',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Novokuznetsk'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True



PROBILL_PATH = '/home/animage/Moon/probill'


MEDIA_ROOT = PROBILL_PATH + '/media/'


MEDIA_URL = '/media/'


STATIC_ROOT = ''

STATIC_URL = '/static/'

if django.VERSION >= (1,4,0):
    ADMIN_MEDIA_PREFIX = '/media/admin/'
else:
    ADMIN_MEDIA_PREFIX = '/static/admin/'


STATICFILES_DIRS = (

)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)



# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


ROOT_URLCONF = 'probill.urls'

TEMPLATE_DIRS = (PROBILL_PATH + '/templates',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'probill.main',
    'probill.billing',
    'probill.nas',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

FLOW_CAT = '/usr/local/bin/flow-cat'
FLOW_STAT = '/usr/local/bin/flow-stat'
FLOW_PATH = '/usr/local/flowdata'

IPFW_PATH = '/sbin/ipfw'
IPFW_MIN_TABLE = 30
IPFW_RULE_STEP = 10
IPFW_START_IN = 21100
IPFW_END_IN = 21800
IPFW_START_OUT = 22100
IPFW_END_OUT = 22800

NETGRAPH_PATH = '/usr/sbin/ngctl'

ARP_PATH = '/usr/sbin/arp'

LOCAL_NAS_ID = 2