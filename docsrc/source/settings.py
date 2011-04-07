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

# Absolute path to the directory containing data for this intance of djity
DATA_DIR = "%s/data" % PROJECT_ROOT

# Djity's themeroller textures and icons directories
TEXTURES_DIR = "%s/images/textures/" % MEDIA_ROOT
ICONS_DIR = "%s/images/icons/" % MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a trailing slash. Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

DAJAXICE_MEDIA_PREFIX="dajaxice" # Will create http://yourdomain.com/dajaxice/...

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+uf*31w)3i8w74)1(^6u%utlfyb^lzu_1_4rqt=+c55v*=lj3g'

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
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.comments',

    #extensions
    'django_extensions',
    'tagging',

    # Dajax
    'dajaxice',
    'dajax',

    #Djity Core
    'djity.portlet',
    'djity.style',
    'djity.portal',
    'djity.project',
    'djity.simplepage',
    'djity.transmeta',
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
)

USE_L10N = True

import re
LOCALE_INDEPENDENT_PATHS = (
    re.compile('^/dajaxice/'),
)

#LOCALEURL_USE_ACCEPT_LANGUAGE = True

FIXTURE_DIRS = 'data/fixtures'

###################################################################
# Import local settings and those from djity apps                 #
###################################################################

# If you want to write over some service or module level configuration, do it
# in local_settings.py

DJITY_APPS = []

DEFAULT_STYLE = []
