#!/usr/bin/env python

from setuptools import setup , find_packages

import djity

setup(name='djity',
    version=djity.version,
    description=djity.description,
    author=djity.author,
    author_email=djity.author_email,
    url=djity.url,
    packages= find_packages(),
    package_data={'djity':[
        'templates/djity/*.html',
        'templates/djity/*/*.html',
        'templates/djity/style/*.css',
        'static/*/*.*',
        'static/*/*/*.*',
        'static/*/*/*/*.*',
        'project_skeleton/*_tmpl',
        'project_skeleton/data/cache/setup_trap',
        'project_skeleton/media/setup_trap',
        'application_skeleton/*.*',
        'application_skeleton/docsrc/*_tmpl',
        'application_skeleton/docsrc/source/*_tmpl',
        'application_skeleton/docsrc/source/*/*_tmpl',
        'application_skeleton/docsrc/source/*/setup_trap',
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

