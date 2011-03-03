#!/usr/bin/python

import djity,shutil,os,sys
from optparse import OptionParser
from skeleton import Skeleton, Var, Bool

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
            Var('admin_name', description="Your name"),
            Var('admin_email', description="Your email address"),
            Bool('debug_toolbar', description="Activate Django debug toolbar ?", default=True)
            ]

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
