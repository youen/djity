import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from djity.core.portal.models import SiteRoot
from djity.core.project.models import Project

class Command(BaseCommand):
    help = "Populate the root of a new djity portal."

    def handle(self, *args, **options):
        # Is there a SiteRoot instance
        site_roots = SiteRoot.objects.all()
        if len(site_roots) > 0:
            logging.error("Instance of SiteRoot found, can't create a new one. Use ./manage.py reset djity.core.portal")
            return

        # Is there a project instance
        projects = Project.objects.all()
        if len(projects) > 0:
            logging.error("Instance of Project found, can't create root. Use ./manage.py reset djity.core.projects")
        
        # Create new site root (there should be only one SiteRoot instance in the base for now)
        site_root = SiteRoot()
        site_root.save()

