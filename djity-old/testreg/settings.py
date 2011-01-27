# -*- coding: utf-8 -*-

import os.path

from logging import debug,info,warn,error


# Get root directory of this instance of DjityPortal
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

###########################
# Django install settings #
###########################

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	# ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
DATABASES = {
	'default':{
	'NAME' : "%s/data/test.db" % PROJECT_ROOT,		 # Or path to database file if using sqlite3.
	'ENGINE' : 'django.db.backends.sqlite3'		   # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'. #todo change
	}
}

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

TEMPLATE_DIRS = (
	"%s/templates" % PROJECT_ROOT,
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.request',
	'django.contrib.messages.context_processors.messages',
)

INSTALLED_APPS = (
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
	'dajax_proxy',

	#tinymce
	'tinymce',

	# Haystack search
	'haystack',

	#Djity Core
	'djity.core.portlet',
	'djity.core.style',
	'djity.core.portal',
	'djity.core.project',
	'djity.core.simplepage',

	#Djity Services
	'djity.services.revtext',
	'djity.services.moatserver',
	#'djity.services.lod',
	'djity.services.transmeta',
	'djity.services.partner',

	# Djity apps
	'djity.modules.wiki',
	'djity.modules.repository',
	'djity.modules.blog',
)

DJITY_MODULES = (
        'djity.modules.blog',
        'djity.modules.wiki',
        'djity.modules.repository',
)

##########################
# Djity install settings #
##########################

#Root project label
ROOT_PROJECT_LABEL = "Djity"

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
	('djity.core.simplepage','home'),
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
	re.compile('^/tinymce/'),
)

#TinyMCE
TINYMCE_JS_URL = '%sjs/tiny_mce/tiny_mce_src.js'%MEDIA_URL
TINYMCE_DEFAULT_CONFIG = {
	'plugins': "",
	'mode':"none",
	'theme': "advanced",
	'theme_advanced_buttons1' : "bold,italic,underline,undo,redo,link,unlink,image,forecolor,styleselect,removeformat,cleanup,code",
	'theme_advanced_buttons3' : "",
	'width' : '100%',
}

TINYMCE_SPELLCHECKER = True
#TINYMCE_COMPRESSOR = True

#LOCALEURL_USE_ACCEPT_LANGUAGE = True

FIXTURE_DIRS = 'data/fixtures'

###################################################
# Import settings from djity services and modules #
###################################################

# Make it automatic by iterating on installed apps ?

from djity.services.partner.settings import *

# If you want to write over some service or module level configuration, do it
# in local_settings.py
try:
    from local_settings import *
except:
    warn('no local settings found')

try:
    from style_settings import *
except:
    warn('no style settings found')


