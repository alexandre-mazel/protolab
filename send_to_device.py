# -*- coding: utf-8 -*-

####
# Send all files and project to a device
# Command line option:
# <scriptname> device_ip
####

import os
import sys

strUserName = "nao" # todo: should be a parameter from the command line
strRemoteHost = sys.argv[1]
strDstPath = "/home/%s/.local/lib/python2.7/site-packages" % strUserName;

os.system( "scp -r protolab/ %s:%s" % (strRemoteHost,strDstPath) );