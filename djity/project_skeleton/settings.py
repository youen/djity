# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
Settings file for an instance of Djity
This file should not be modified: use local_settings.py instead
"""

import os
from logging import debug,info,warn,error
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

##########################
# Djity install settings #
##########################

# Default roles and permissions are used at the creation of a Djity project
# They can be edited online afterward
# Generic roles ('manager','anyone' and 'public') don't to be declared here
# 'anyone' stands for 'any member of the project', 'public' means really anyone
DEFAULT_ROLES = [
    ('contributor',"Project contributor"),
    ('user',"Project user"),
]

# manager implicitly has all permissions
DEFAULT_PERMISSIONS = {
    'view':("Permission to navigate in the project's page",['anyone']),
    'edit':("Permission to edit project's content",['contributor']),
    'upload':("Permission to put and delete files and documents",['contributor']),
    'manage':("Permission to perform administration tasks on the project",[]),
}

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
# Import local settings and those from djity services and modules #
###################################################################

# If you want to write over some service or module level configuration, do it
# in local_settings.py

DJITY_MODULES = open("%s/modules.txt" % PROJECT_ROOT).read().split('\n')
DJITY_MODULES.remove('')
DJITY_SERVICES = open("%s/services.txt" % PROJECT_ROOT).read().split('\n')
DJITY_SERVICES.remove('')

djity_apps = list(DJITY_MODULES + DJITY_SERVICES)

# add activated djity modules and services to installed apps
if len (djity_apps) >= 0:
    INSTALLED_APPS += djity_apps

def create_link(media_path,media_link):
    """
    create links to build a virtually unified media directory
    """
    if os.path.isdir(media_path) and not os.path.exists(media_link):
        os.symlink(media_path,media_link)
        print("create link to %s in %s" % (media_path, media_link))

# create links for all directories in djity-core media dir
djity_media = DJITY_ROOT+"/media"
for d in os.listdir(djity_media):
    create_link(djity_media+"/"+d,MEDIA_ROOT+"/"+d)

# import djity apps separate settings
# add their templates to the list
# and create links to their media directories
for app in djity_apps:
    try:
        print("import settings from %s.settings" % app)
        exec("from %s.settings import *" % app)
    except:
        print("no module %s.settings" % app)
        
    try:
        print("get path of application %s" % app)
        exec("from %s import __path__ as app_path" % app)
        app_path = app_path[0]
        print "-> %s" % app_path
    except Exception,e:
        warn(e)
        continue

    try:
        templates_path = app_path+"/templates"
        if os.path.isdir(templates_path):
            TEMPLATE_DIRS.append(templates_path)
            print("get templates from %s" % templates_path)

        media_path = app_path+"/media"
        media_link = MEDIA_ROOT+"/"+app
        create_link(media_path,media_link)
    except Exception,e:
        warn(e)

# import and overwrite all settings defined locally
try:
    from local_settings import *
except:
    warn('no local settings found')

# apply django debug toolbar if specified in settings
try:
    dt = DEBUG_TOOLBAR
except:
    warn("no parameter 'debug_toolbar' found in settings")
    dt = False

if dt:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    # debug toolbar will only work locally
    INTERNAL_IPS = ('127.0.0.1',)
    INSTALLED_APPS += ('debug_toolbar',)

# import settings specific to theme management
try:
    from style_settings import *
except:
    warn('no style settings found')


