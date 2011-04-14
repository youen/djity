#!/usr/bin/env python

from setuptools import setup , find_packages

setup(name='djity',
    version='0.2',
    description='A versatile portal for Web applications and projects based on Django',
    author='Team Djity',
    author_email='contact@djity.net',
    url='http://redmine.djity.net/projects/djityportal',
    packages= find_packages(),
    package_data={'djity':[
        'templates/djity/*.html',
        'templates/djity/*/*.html',
        'templates/djity/style/*.css',
        'media/*/*.*',
        'media/*/*/*.*',
        'media/*/*/*/*.*',
        'project_skeleton/*_tmpl',
        'project_skeleton/data/cache/setup_trap',
        'project_skeleton/media/setup_trap',
        'application_skeleton/*.*',
        'application_skeleton/{package_name}/*_tmpl',
        'application_skeleton/{package_name}/media/js/setup_trap',
        'application_skeleton/{package_name}/media/css/setup_trap',
        'application_skeleton/{package_name}/media/images/setup_trap',
        'application_skeleton/{package_name}/templatetags/setup_trap',
        'application_skeleton/{package_name}/templates/{package_name}/*.html',
        ]},
    scripts=['scripts/djity-admin.py'],
	requires=['django (>=1.2)','dajax (>=0.8.4)','skeleton (>=0.6)'],
)

