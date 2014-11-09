import django
from ConfigParser import RawConfigParser

config = RawConfigParser()

config.read('settings.conf.default')
config.read('/etc/probill/settings.conf')
config.read('/usr/local/etc/probill/settings.conf')

DATABASES = {
    'default': {
        'USER': config.get('database', 'DATABASE_USER'),
        'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
        'HOST': config.get('database', 'DATABASE_HOST'),
        'PORT': config.get('database', 'DATABASE_PORT'),
        'ENGINE': config.get('database', 'DATABASE_ENGINE'),
        'NAME': config.get('database', 'DATABASE_NAME'),
    }
}

if config.has_option('database', 'DATABASE_FOR_MERGE'):
    DATABASES.update({
        'merge_from': {
            'USER': config.get('database', 'DATABASE_USER'),
            'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
            'HOST': config.get('database', 'DATABASE_HOST'),
            'PORT': config.get('database', 'DATABASE_PORT'),
            'ENGINE': config.get('database', 'DATABASE_ENGINE'),
            'NAME': config.get('database', 'DATABASE_FOR_MERGE'),
    }
    })

DEBUG = config.getboolean('debug','DEBUG')
TEMPLATE_DEBUG = config.getboolean('debug','TEMPLATE_DEBUG')


TIME_ZONE = config.get('main', 'TIME_ZONE')
LANGUAGE_CODE = config.get('main', 'LANGUAGE_CODE')
SITE_ID = config.getint('main', 'SITE_ID')
SECRET_KEY = config.get('main','SECRET_KEY')

# Probill custom settings
PROBILL_PATH = config.get('probill', 'PROBILL_PATH')

# Billing vars
TRUST_DAYS_COUNT = config.getint('billing', 'TRUST_DAYS_COUNT')

## Program path
FLOW_CAT = config.get('prog_path', 'FLOW_CAT')
FLOW_STAT = config.get('prog_path', 'FLOW_STAT')
FLOW_PATH = config.get('prog_path', 'FLOW_PATH')
IPFW_PATH = config.get('prog_path', 'IPFW_PATH')
NETGRAPH_PATH = config.get('prog_path', 'NETGRAPH_PATH')
ARP_PATH = config.get('prog_path', 'ARP_PATH')
PING_PATH = config.get('prog_path', 'PING_PATH')
ROUTE_PATH = config.get('prog_path', 'ROUTE_PATH')
SUDO_PATH = config.get('prog_path', 'SUDO_PATH')

## IPFW settings
IPFW_MIN_TABLE = config.getint('ipfw', 'IPFW_MIN_TABLE')
IPFW_RULE_STEP = config.getint('ipfw', 'IPFW_RULE_STEP')
IPFW_START_IN = config.getint('ipfw', 'IPFW_START_IN')
IPFW_END_IN = config.getint('ipfw', 'IPFW_END_IN')
IPFW_START_OUT = config.getint('ipfw', 'IPFW_START_OUT')
IPFW_END_OUT = config.getint('ipfw', 'IPFW_END_OUT')
IPFW_QUEUE_SIZE = config.getint('ipfw', 'IPFW_QUEUE_SIZE')

IPFW_NAT_TABLE= config.getint('ipfw', 'IPFW_NAT_TABLE')
IPFW_NAT_START = config.getint('ipfw', 'IPFW_NAT_START')
IPFW_NAT_END = config.getint('ipfw', 'IPFW_NAT_END')
IPFW_INCLUDE = config.get('ipfw', 'IPFW_INCLUDE')

## NAS setting
LOCAL_NAS_ID = config.getint('nas', 'LOCAL_NAS_ID')

OSMP_ENABLE = False
if config.has_section('osmp'):
    OSMP_MIN_SUM = config.getint('osmp', 'OSMP_MIN_SUM')
    OSMP_MAX_SUM = config.getint('osmp', 'OSMP_MAX_SUM')
    OSMP_ENABLE = config.getboolean('osmp', 'OSMP_ENABLE')

MEDIA_ROOT = PROBILL_PATH + '/media/'
MEDIA_URL = '/media/'


STATIC_ROOT = ''

STATIC_URL = '/static/'

if django.VERSION >= (1,4,0):
    ADMIN_MEDIA_PREFIX = '/media/admin/'
else:
    ADMIN_MEDIA_PREFIX = '/static/admin/'

USE_I18N = True
USE_L10N = True


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
    'dojango',
    'moon',
    'main',
    'billing',
    'nas',
    'mptt',
    'south',
    'iptv'
)


LOGIN_URL = '/moon/login'
LOGOUT_URL = '/moon/logout'
LOGIN_REDIRECT_URL = '/moon'

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

if config.has_section('userside'):
    INSTALLED_APPS = INSTALLED_APPS + ('userside',)
    DATABASES.update({
        'userside': {
            'USER': config.get('userside', 'DATABASE_USER'),
            'PASSWORD': config.get('userside', 'DATABASE_PASSWORD'),
            'HOST': config.get('userside', 'DATABASE_HOST'),
            'PORT': config.get('userside', 'DATABASE_PORT'),
            'ENGINE': config.get('userside', 'DATABASE_ENGINE'),
            'NAME': config.get('userside', 'DATABASE_NAME'),
            }
    })
    if config.has_option('userside', 'EXTRA_FIELDS'):
        def sx(x): return x.split(',')
        EXTRA_FIELDS = map(sx, [f for f in config.get('userside', 'EXTRA_FIELDS').split(';') if f])
    else:
        EXTRA_FIELDS = []

if config.has_section('client_side'):
    TEMPLATE_DIRS = TEMPLATE_DIRS + (config.get('client_side', 'TEMPLATE_DIR'),)

if config.has_section('http_redirect'):
    REDIRECT_TO = config.get('http_redirect', 'REDIRECT_TO')
else:
    REDIRECT_TO = ''

if config.has_section('visa_gpb'):
    VISA_ENABLE = True
    VISA_MERCHANT_ID = config.get('visa_gpb', 'VISA_MERCH_ID')
    VISA_PAY_URL = config.get('visa_gpb', 'VISA_PAY_URL')
else:
    VISA_ENABLE = False
    VISA_MERCHANT_ID = ''
    VISA_PAY_URL = ''

if config.has_section('rib'):
    RIB_ENABLE = True
    RIB_URL = config.get('rib', 'RIB_URL')
    RIB_INN = config.get('rib', 'RIB_INN')
    RIB_OGRN = config.get('rib', 'RIB_OGRN')
    RIB_ORG_NAME = config.get('rib', 'RIB_ORG_NAME')
    RIB_EMAIL = config.get('rib', 'RIB_EMAIL')
    RIB_CERT_PATH = config.get('rib', 'RIB_CERT_PATH')
    TMP_PATH = config.get('rib', 'TMP_PATH')
    OPENSSL_COMMAND = config.get('rib', 'OPENSSL_COMMAND')
    if config.has_option('rib', 'RIB_VERSION'):
        RIB_VERSION = config.get('rib', 'RIB_VERSION')
    else:
        RIB_VERSION = ''
    OPENSSL_COMMAND = config.get('rib', 'OPENSSL_COMMAND')
else:
    RIB_ENABLE = True
    RIB_URL = ''
    RIB_INN = ''
    RIB_OGRN = ''
    RIB_ORG_NAME = ''
    RIB_EMAIL = ''
    RIB_CERT_PATH = ''
    TMP_PATH = ''
    OPENSSL_COMMAND = ''
    RIB_VERSION = ''


if config.has_section('lanbilling'):
    INSTALLED_APPS = INSTALLED_APPS + ('lb',)
    LB_ENABLE = True
    LB_NAS_ID = config.get('lanbilling', 'LB_NAS_ID')
    LB_PREF_SRC = config.get('lanbilling', 'LB_PREF_SRC')
    LB_SOAP_URL = config.get('lanbilling', 'LB_SOAP_URL')
    LB_USERNAME = config.get('lanbilling', 'LB_USERNAME')
    LB_PASSWORD = config.get('lanbilling', 'LB_PASSWORD')
    LB_AGENT_TYPE = config.get('lanbilling', 'LB_AGENT_TYPE')
else:
    LB_ENABLE = False
    LB_NAS_ID = ''
    LB_PREF_SRC = ''
    LB_SOAP_URL = ''
    LB_USERNAME = ''
    LB_PASSWORD = ''
    LB_AGENT_TYPE = ''

NEW_QOS = False
SQ_PACKET_MARKS = ['no-mark']
SQ_BURST_TIMEOUT = 0
SQ_BURST_MULTI = 0
SQ_QUEUE_TYPE = 'hotspot-default'

if config.has_section('qos'):
    NEW_QOS = config.getboolean('qos', 'NEW_QOS')
    if config.has_option('qos', 'PACKET_MARKS'):
        SQ_PACKET_MARKS = config.get('qos', 'PACKET_MARKS').split(',')
    if config.has_option('qos', 'BURST_TIMEOUT'):
        SQ_BURST_TIMEOUT = config.get('qos', 'BURST_TIMEOUT')
    if config.has_option('qos', 'BURST_MULTI'):
        SQ_BURST_MULTI = config.get('qos', 'BURST_MULTI')
    if config.has_option('qos', 'QUEUE_TYPE'):
        SQ_QUEUE_TYPE = config.get('qos', 'QUEUE_TYPE')

