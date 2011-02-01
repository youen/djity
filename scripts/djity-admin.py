#!/usr/bin/python

import djity,shutil,os,sys
from optparse import OptionParser
from skeleton import Skeleton, Var

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
    vars = []

class ModuleSkeleton(Skeleton):
    src = djity.__path__[0]+'/module_skeleton'
    vars = []

# execute command create_project
if command == 'create_project':
    sys.argv[0] += ' create_project'
    sys.argv.remove('create_project')
    ProjectSkeleton.cmd()

# execute command create_project
if command == 'create_module':
    sys.argv[0] += ' create_module'
    sys.argv.remove('create_module')
    ModuleSkeleton.cmd()
