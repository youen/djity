#!/usr/bin/env python

from setuptools import setup , find_packages

setup(name='djity',
    version='0.2',
    description='A versatile portal for Web applications and projects based on Django',
    author='Team Djity',
    author_email='contact@djity.net',
    url='http://redmine.djity.net/projects/djityportal',
    packages= find_packages(),
    package_data={'djity':['templates/*/*/*','media/*/*/*/*','locale/*','tools/*','project_skeleton/*']},
    scripts=['scripts/djity-admin.py'],
	requires=['django (>=1.2)','dajax (>=0.8.4)','skeleton (>=0.6)'],
)

