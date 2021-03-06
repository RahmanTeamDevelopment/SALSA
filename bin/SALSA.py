#!env/bin/python

import main
from optparse import OptionParser
import os
import sys
from sys import argv
from main.version import __version__
from main.topex import run_topex

#fix scriptdir so that it points to the path of SALSA and not SALSA/env/bin/
scriptdir=os.path.dirname(os.path.realpath(__file__))
scriptdir=scriptdir[:-7]

if not os.path.isdir(scriptdir+"/config_files/"):
	sys.exit("Error: No default configurations directory %s. Please configure SALSA by running 'configure.py' before using SALSA" % (scriptdir+"/config_files/"))
if not os.path.isfile(scriptdir+"/config_files/cava_config.txt"):
	sys.exit("Error: No CAVA configuration file.  Please configure SALSA by running 'configure.py' before using SALSA")
if not os.path.isfile(scriptdir+"/config_files/coverview_config.json"):
	sys.exit("Error: No CoverView configuration file.  Please configure SALSA by running 'configure.py' before using SALSA")
if not os.path.isfile(scriptdir+"/config_files/topex_config.ini"):
	sys.exit("Error: No TOpEx configuration file.  Please configure SALSA by running 'configure.py' before using SALSA")

####################################################################################
##
## Add script to check files+paths for all files mentioned in config files.
## Add script to check files are in the right format!!!
##
####################################################################################

output_error_message = "\n\nInvalid usage: use SALSA as follows:\n\nsalsa TOpEx [Options]\nsalsa DeCON [Options]\nsalsa QUIC [Options]\n\n"
if len(argv) <= 1:
	sys.exit(output_error_message)

if argv[1] == "TOpEx":
	run_topex(argv)
elif argv[1] == "DeCON":
	print "WORKING ON IT!!!!!!!!!!"
elif argv[1] == "QUIC":
	print "WORKING ON IT!!!!!!!!!!"
else:
	sys.exit(output_error_message)

