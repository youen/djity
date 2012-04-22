#!/usr/bin/python

import djity,shutil,os,sys,random, os.path
from optparse import OptionParser
from skeleton import Skeleton, Var, Bool
from subprocess import Popen,call,PIPE
from django.utils.importlib import import_module

commands = ['create_project','create_app','ls_apps']
commands_help = {
        'create_project':"Create a new Djity project in the specified directory",
        'ls_apps':"List all Djity applications installed on this machine",
        'create_app':"Create a new almost empty Djity application for developpers",
        }

# if no valid command was specified, display help accordingly
if len(sys.argv)<=1 or not sys.argv[1] in commands:
    usage = "Usage: %prog subcommand [options] [args]\nAvailable subcommands:"
    for command in commands:
        usage += "\n\t%s - %s" % (command,commands_help[command])

    parser = OptionParser(usage)
    (options, args) = parser.parse_args()
    parser.error("A valid subcommand is required")
    exit()

command = sys.argv[1]

def ls_apps():
    """
    Find all available djity applications on the system
    """
    apps = set()
    for path in sys.path:
        try:
            packages = os.listdir(path)
        except:
            continue
        for package in packages:
            if package.startswith('djity_'):
                # remove information related to eggs
                package = package.split('.')[0]
                package = package.split('-')[0]
                try:
                    exec("import %s" % package)
                except:
                    continue
                apps.add(package)
    return apps

class ProjectSkeleton(Skeleton):
    src = djity.__path__[0]+'/project_skeleton'
    variables = [
            Var('project_label', description="The label of the root project of this instance of Djity", default="Djity"),
            Var('admin_name', description="Your name", default="admin"),
            Var('admin_email', description="Your email address", default="admin@example.com"),
            Var('admin_password', description="Your password", default="admin"),

            Bool('develop', description="Build and run a default development project server and activate debug options (logging, templates and debug toolbar) ", default=False),
            ]
       
    def run(self, dst_dir, run_dry=False):
        """
        overwrite the standard run method from Skeleton.
        If the option develop is activated, build the project with default
        development parameters.
        """

        # add a boolean variable for each available djity application
        # on the system
        apps = ls_apps()
        for app in apps:
            self.variables.append(Bool(app, description="Install this application",default=True))

        # use Skeleton to ask user's input
        self.get_missing_variables()

        # Generate a secret key in the same way django-admin does
        self['secret_key'] = ''.join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])

        # The path to the project directory
        self['project_path'] = os.path.abspath(dst_dir)

        # The path to the virtual environement
        self['virtualenv_path'] = os.__file__[:-20]

        # use skeleton to write the target directory
        self.write(dst_dir, run_dry=run_dry, ignore=['setup_trap'])

        # derive apps list from the user's input
        apps = filter(lambda a:self[a],apps)
        
        for app in apps:
            print "run 'manage.py install_app %s'" % app
            call("python manage.py install_app %s" % app,shell=True,cwd=dst_dir)

        print "setup a bare project in %s" % dst_dir
        if self['develop']:
            print "make it ready for quick development..."
            sys.path = [dst_dir] + sys.path
            os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' 
            from django.core.management import call_command
            from django.contrib.auth.models import User
            from django.db.utils import IntegrityError
            print "create tables"
            call_command('syncdb', interactive=False)
            print "define superuser '%s'" % self['admin_name']
            try:
                my_admin = User.objects.create_superuser(self['admin_name'], self['admin_email'], self['admin_password'])
            except IntegrityError :
                print "superuser already defined"
                
            print "install indexes"
            print "run 'manage.py create_portal'"
            call_command('create_portal', interactive=False)
            #print "run 'manage.py runserver'"
            #call("python manage.py runserver",shell=True,cwd=dst_dir)


class ApplicationSkeleton(Skeleton):
    src = djity.__path__[0]+'/application_skeleton'
    variables = [
            Var('application_name',description="Package, module and class names will be derived from it"),
            Var('author_name',description="Your name, or the name of the developers team",default=""),
            Var('author_email',description="An email address to contact the developer(s)",default=""),
            Var('url',description="The official page",default=""),
            Var('description',description="A short description of this application, you should probably write more detailed information in the README file",default=""),
            ]
    def run(self, dst_dir, run_dry=False):
        """
        overwrite the standard run method from Skeleton.
        Get rif of whitespaces in module name.
        Add a 'class_name' var by uppercasing the first letter of 'module_name'.
        """
        # use Skeleton to ask user's input
        self.get_missing_variables()
        
        # derive automatic parameters from user defined application name
        self['class_name'] = ''.join([word[0].upper()+word[1:] for word in self['application_name'].lower().split(' ')])
        print 'Class Name -> %s' % self['class_name']
        self['module_name'] = self['class_name'].lower()
        print 'Module Name -> %s' % self['module_name']
        self['package_name'] = "djity_%s" % self['module_name']
        print 'Package Name -> %s' % self['package_name']
        # use skeleton to write the target directory
        self.write(dst_dir, run_dry=run_dry, ignore=['setup_trap'])
        print 'You might want to do something like:'
        print '> cd %s' % dst_dir
        print '> python setup.py develop'
        print '> djity-admin.py ls_apps'
        print "Then you may create a new project using 'djity-admin.py create_project'..."
        print "...Or install the application in an existing project"
        print '> cd /path/to/project/'
        print '> python manage.py install_app %s' % self['package_name']
        print '> python manage.py syncdb'

# execute command create_project
if command == 'create_project':
    sys.argv[0] += ' create_project'
    sys.argv.remove('create_project')
    ProjectSkeleton.cmd()

# execute command create_module
if command == 'create_app':
    sys.argv[0] += ' create_app'
    sys.argv.remove('create_app')
    ApplicationSkeleton.cmd()

# display the list of Djity applications currently installed on this machine
if command == 'ls_apps':
    for app in ls_apps():
        app_module = import_module(app)
        line = app
        if app_module.__dict__.get('pip_name','') != '':
            line += " - on pip: %s" % app_module.pip_name
        if app_module.__dict__.get('version','') != '':
            line += " v%s" % app_module.version
        if app_module.__dict__.get('author','') != '':
            line += " - %s" % app_module.author
        if app_module.__dict__.get('author_email','') != '':
            line += " <%s>" % app_module.author_email
        if app_module.__dict__.get('url','') != '':
            line += "\n\t%s" % app_module.url
        if app_module.__dict__.get('description','') != '':
            line += "\n\t%s" % app_module.description
        print line

