# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import json
from django.utils import unittest
from django.test.client import Client
from djity.project.models import Project
import djity 

class ProjectTest(unittest.TestCase):
    fixtures = [djity.__path__[0]+'/fixtures/test_project.json']

    def setUp(self):
        # Every test needs a client.
        self.client = Client()


    def test_login(self):
        """
        Test the login
        """
        argv = {
                'js_traget':'document',
                'path':'',
                'username':'admin',
                'password':'admin',
                'project_name':'root',
                'module_name':'home',
                'LANGUAGE_CODE':'fr'
                }
        Project.objects.get(name='root')
        response = self.client.post('/dajaxice/djity.portal.login/',{'callback':'Dajax.process','argv':json.dumps(argv)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['username'], 'admin')

        



