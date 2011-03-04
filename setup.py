#!/usr/bin/env python

from distutils.core import setup

setup(name='djity',
    version='1.0',
    description='A versatile portal for Web applications and projects based on Django',
    author='Team Djity',
    author_email='contact@djity.net',
    url='http://redmine.djity.net/projects/djityportal',
    packages=['djity',
		'djity.core',
		'djity.core.portal',
		'djity.core.portlet',
		'djity.core.project',
		'djity.core.style',
		'djity.core.simplepage',
		'djity.utils',
		'djity.modules',
		'djity.services'],
    package_dir={'djity':'.'},
    package_data={'djity':['templates/*/*/*',
		'media/*/*/*/*',
		'locale/*',
		'tools/*',
		'README',
		'project_skeleton/*']},
    scripts=['scripts/djity-admin.py'],
)
