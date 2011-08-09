# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
Settings file for an instance of Djity
This file should not be modified: use local_settings.py instead
"""

import os
from logging import debug,info,warn,error
from django.utils.importlib import import_module
import djity

# Get root directory of this instance of Djity
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DJITY_ROOT = djity.__path__[0]

###########################
# Django install settings #
###########################

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Local time zone for this installation. Choices can be found here: http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your system time zone.
TIME_ZONE = 'America/Chicago'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not to load the internationalization machinery.
USE_I18N = True

USE_L10N = True
DATE_FORMAT = None
TIME_FORMAT = None 
# Absolute path to the directory that holds media. Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = "%s/media" % PROJECT_ROOT
STATIC_ROOT = "%s/static" % PROJECT_ROOT

# Absolute path to the directory containing data for this intance of djity
DATA_DIR = "%s/data" % PROJECT_ROOT

# Djity's themeroller textures and icons directories
TEXTURES_DIR = "%s/djity/images/textures/" % STATIC_ROOT
ICONS_DIR = "%s/djity/images/icons/" % STATIC_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'
STATIC_URL = '/site_static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a trailing slash. Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

DAJAXICE_MEDIA_PREFIX="dajaxice" # Will create http://yourdomain.com/dajaxice/...

# Make this unique, and don't share it with anybody.
SECRET_KEY = 't%u=6xy3=1bhbf$2us1ekf4l8o(jiq_-!m&j=&ckd0u03dfh(1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'localeurl.middleware.LocaleURLMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = [DJITY_ROOT+"/templates",]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
)

INSTALLED_APPS = [
    #overwrite url dispatcher with localeurl
    'localeurl',
    
    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.comments',
    'django.contrib.staticfiles',

    #extensions

    # Dajax
    'dajaxice',
    'dajax',

    # Haystack for search
    'haystack',

    #Djity Core
    'djity',
    'djity.portlet',
    'djity.style',
    'djity.portal',
    'djity.project',
    'djity.simplepage',
    'djity.transmeta',
    'djity.search',
]

###########################################
# Djity roles and permissions definitions #
###########################################

# Role values are defined in constants
ANONYMOUS = 0
AWAITING = 1
USER = 2
CONTRIBUTOR = 3
MANAGER = 4

# Module status values as well
DRAFT = 0
PRIVATE = 1
PUBLIC = 2

# permissions are associated with the minimal value
# or role needed to grant them
PERMISSION_MIN_ROLE = {
    'view_public':ANONYMOUS,
    'view_private':USER,
    'edit':CONTRIBUTOR,
    'upload':CONTRIBUTOR,
    'manage':MANAGER,
}

# generic permission names can lead to different actual
# permissions according on the status of the current module
STATUS_PERMISSIONS = {
    DRAFT:{'view':'edit'},
    PRIVATE:{'view':'view_private'},
    PUBLIC:{'view':'view_public'}
}

# list of permissions to check when updating djity's context
PERMISSIONS = ['view','edit','upload','manage']

# List of visible statuses according to role (used to filter search results)
HIDDEN_STATUSES = {
    ANONYMOUS:[DRAFT,PRIVATE],
    AWAITING:[DRAFT,PRIVATE],
    USER:[DRAFT],
    CONTRIBUTOR:[],
    MANAGER:[],
}

# Status display in user interface
STATUS_DISPLAY = [[DRAFT,'Draft'],[PRIVATE,'Private'],[PUBLIC,'Public']]

# role display in UI
ROLES_DISPLAY = [
        (ANONYMOUS,'Anonymous'),
        (AWAITING,'Awaiting'),
        (USER ,'User'),
        (CONTRIBUTOR,'Contributor'),
        (MANAGER,'Manager'),
        ]


##########################
# Djity install settings #
##########################

# Djity project modules declarations
DEFAULT_PROJECT_MODULES = [
    ('djity.simplepage','home'),
]

# Language code for this installation. All choices can be found here: http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'
DEFAULT_CHARSET = 'utf-8'
ugettext = lambda s: s # dummy ugettext function, as django's docs say

LANGUAGES = (
    ('en', ugettext(u'English')),
    ('fr', ugettext(u'Français')),
    ('zh', ugettext(u'中文')),
)

USE_L10N = True

import re
LOCALE_INDEPENDENT_PATHS = (
    re.compile('^/dajaxice/'),
)

#LOCALEURL_USE_ACCEPT_LANGUAGE = True

FIXTURE_DIRS = 'data/fixtures'

###########################
# Djity indexing settings #
###########################

# Haystack search engine connections configuration
HAYSTACK_CONNECTIONS = {'default':{
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': '%s/data/whoosh/djity_index/default' % (PROJECT_ROOT),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    }
}

for (language,language_repr) in LANGUAGES:
    HAYSTACK_CONNECTIONS['default_'+language] = {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': '%s/data/whoosh/djity_index/%s' % (PROJECT_ROOT,language),
        'STORAGE': 'file',
        'POST_LIMIT': 128 * 1024 * 1024,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'LANGUAGE': '%s' % language
    }
    
HAYSTACK_ROUTERS = ['haystack.routers.LanguageRouter']

###################################################################
# Import local settings and those from djity apps                 #
###################################################################

# If you want to write over some service or module level configuration, do it
# in local_settings.py

DJITY_APPS = []
DEFAULT_STYLE = []


