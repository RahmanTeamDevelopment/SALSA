#!env/bin/python

import main
import optparse
import OptionParser
from main.version import __version__
import os

scriptdir=os.path.dirname(os.path.realpath(__file__))

if not os.path.isfile(scriptdir+"/config_files/cava_config.txt"):
	sys.exit("Error: No CAVA configuration file.  Please run 'configure.py' before running SALSA")
if not os.path.isfile(scriptdir+"/config_files/coverview_config.json"):
	sys.exit("Error: No CoverView configuration file.  Please run 'configure.py' before running SALSA")
	
	

