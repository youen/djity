#!/usr/bin/python

import djity,shutil,os
from optparse import OptionParser

parser = OptionParser("usage: %prog project_directory")

(options, args) = parser.parse_args()

if len(args) == 0:
    parser.error("argument 'project_directory' is required")

project_path = args[0]
skeleton_path =  djity.__path__[0]+'/project_skeleton'

print "Copy %s > %s" % (skeleton_path,project_path)

shutil.copytree(skeleton_path,project_path)
os.makedirs("%s/data/cache" % project_path)
os.makedirs("%s/media" % project_path)
