# -*- coding: utf-8 -*-

"""
local settings for an instance of Djity
For more parameters to modify, check settings.py
"""

import os.path

# Get root directory of this instance of Djity
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
	# ('Your Name', 'your_email@domain.com'),
)

ROOT_PROJECT_LABEL = "Djity"

DATABASES = {
	'default':{
	'NAME' : "%s/data/test.db" % PROJECT_ROOT, # Name of base or path to database file if using sqlite3.
	'ENGINE' : 'django.db.backends.sqlite3', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'. #todo change
#	'USER' : 'djityportal', # not required with sqlite
#	'PASSWORD': 'zdsqomlk', # not required with sqlite
	}
}

DJITY_MODULES = (
    #'djityblog',
    #'djitywiki',
    #'djityrepository',
)

DJITY_SERVICES = (
	#'djityrevtext',
	#'djitymoatserver',
	#'djitylod',
	#'djity.services.partner',
)

