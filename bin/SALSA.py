#!env/bin/python

import main
import optparse
import OptionParser
from main.version import __version__
import os

scriptdir=os.path.dirname(os.path.realpath(__file__))

if not os.path.isdir(scriptdir+"/config_files/"):
	sys.exit("Error: No directory %s. Please configure SALSA by running 'configure.py' before using SALSA")
if not os.path.isfile(scriptdir+"/config_files/cava_config.txt"):
	sys.exit("Error: No CAVA configuration file.  Please configure SALSA by running 'configure.py' before using SALSA")
if not os.path.isfile(scriptdir+"/config_files/coverview_config.json"):
	sys.exit("Error: No CoverView configuration file.  Please configure SALSA by running 'configure.py' before using SALSA")
if not os.path.isfile(scriptdir+"/config_files/topex_config.ini"):
	sys.exit("Error: No TOpEx configuration file.  Please configure SALSA by running 'configure.py' before using SALSA")


print "WORKING ON IT!!!!!!!!!!"
