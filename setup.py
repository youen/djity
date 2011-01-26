#!/usr/bin/env python

from setuptools import setup

setup(name='djity',
    version='0.2',
    description='A versatile portal for Web applications and projects based on Django',
    author='Team Djity',
    author_email='contact@djity.net',
    url='http://redmine.djity.net/projects/djityportal',
    packages=['djity',
		      'djity.core',
			  'djity.core.portlet',
			  'djity.core.portal',
			  'djity.core.project',
			  'djity.core.simplepage',
			  'djity.core.style',
			  'djity.utils',
			  'djity.modules',
			  'djity.services'],
	package_dir={'djity':'.'},
    package_data={'djity':['templates/*/*/*','media/*/*/*/*','locale/*','tools/*','README','project_skeleton/*']},
    scripts=['scripts/djity-admin.py'],
)
