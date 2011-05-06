import logging,os

from django.core.management.base import BaseCommand
from django.utils.importlib import import_module

from django.conf import settings

from djity.utils import create_link

class Command(BaseCommand):
    args = '<app>'
    help = """Install an application in the current project.\
 The application must already be installed in the system.\
 Use 'djity-admin.py ls_apps' to findout which Djity applications\
 are available on this machine."""

    def handle(self, *args, **options):
        try:
            app = args[0]
        except:
            logging.error("No application in arguments, check usage with '--help'")
            return
        try:
            # get the path of the python package for the current app
            app_path = import_module(app).__path__
            app_path = app_path[0]
        except Exception,e:
            logging.error("The application %s wasn't found in the path. You shoud use 'djity-admin.py ls_apps'." % app)
            return

        apps_path = "%s/apps.txt" % settings.PROJECT_ROOT
        if not os.path.isfile(apps_path):
            logging.warning("File %s is missing and needed to install new apps. We shall create it.")
            open(apps_path,'c').close()

        with open(apps_path,'r') as apps_file:
            installed_apps = set(apps_file.read().split('\n'))

        if app in installed_apps:
            logging.warning("Application %s is already declared as installed" % app)
        else:
            logging.info("Write %s in %s" % (app,apps_path))
            with open(apps_path,'a') as apps_file:
                apps_file.write("%s\n" % app)

        # if necessary create link to this app's static directory (for develop mode)
        static_path = app_path+"/static"
        static_link = settings.STATIC_ROOT+"/"+app
        create_link(static_path,static_link)

        print "Application %s is installed.\nYou should use 'python manage.py sync_db'" % app
