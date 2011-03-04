#!/usr/bin/python

import djity,shutil,os,sys
from optparse import OptionParser
from skeleton import Skeleton, Var, Bool
from subprocess import Popen,call,PIPE

commands = ['create_project','create_module']

# if no valid command was specified, display help accordingly
if len(sys.argv)<=1 or not sys.argv[1] in commands:
    usage = "Usage: %prog subcommand [options] [args]\nAvailable subcommands:"
    for command in commands:
        usage += "\n\t%s" % command

    parser = OptionParser(usage)
    (options, args) = parser.parse_args()
    parser.error("A valid subcommand is required")
    exit()

command = sys.argv[1]

class ProjectSkeleton(Skeleton):
    src = djity.__path__[0]+'/project_skeleton'
    variables = [
            Var('project_label', description="The label of the root project of this instance of Djity", default="Djity"),
            Var('admin_name', description="Your name", default="admin"),
            Var('admin_email', description="Your email address", default="admin@example.com"),
            Bool('debug_toolbar', description="Activate Django debug toolbar ?", default=False),
            Bool('develop', description="Build and run a default development project server", default=False),
            ]
       
    def run(self, dst_dir, run_dry=False):
        """
        overwrite the standard run method from Skeleton.
        If the option develop is activated, build the project with default
        development parameters.
        """
        Skeleton.run(self, dst_dir, run_dry)
        if self['admin_name']:
            print "setup a default developement project..."
            p = Popen("./manage.py syncdb",stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True,cwd=dst_dir)
            print "create links for media directories in %s/media" % dst_dir
            print "create tables"
            print "define superuser '%s'" % self['admin_name']
            p.communicate("yes\n%s\n%s\n" % (self['admin_name'],self['admin_email']))
            print "install indexes"
            print "run 'manage.py create_portal'"
            call("./manage.py create_portal",shell=True,cwd=dst_dir)
            print "run 'manage.py runserver'"
            call("./manage.py runserver",shell=True,cwd=dst_dir)


class ModuleSkeleton(Skeleton):
    src = djity.__path__[0]+'/module_skeleton'
    variables = []



# execute command create_project
if command == 'create_project':
    sys.argv[0] += ' create_project'
    sys.argv.remove('create_project')
    ProjectSkeleton.cmd()

# execute command create_module
if command == 'create_module':
    sys.argv[0] += ' create_module'
    sys.argv.remove('create_module')
    ModuleSkeleton.cmd()
