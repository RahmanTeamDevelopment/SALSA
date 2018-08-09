#!env/bin/python

from optparse import OptionParser
from subprocess import call
import os
import sys
from main.version import __version__
from main import generate
from main import parse_ini


##############################################################################################################
##############################################################################################################
#              Things to add
# 1) right now this is only set up to work for GRCh37.  Need to add GRCh38 functionality
##############################################################################################################
##############################################################################################################

# Current directory
scriptdir=os.path.dirname(os.path.realpath(__file__))

# Command line argument parsing
parser = OptionParser(description='Configure script for SALSA v{}'.format(__version__), usage='configure_salsa.py <options>', version=__version__)
parser.add_option('--reference', default=None, dest='reference', action='store', help="Required: Input reference file (GRCh37) [default value: %default]")
parser.add_option('--bed', default=None, dest='bed', action='store', help="Required: BED file containing the targeted regions (exons/genes) to use for CoverView/QSM [default value: %default]")
parser.add_option('--salsa_config', default=scriptdir+"/default.ini", dest='salsa_config', action='store', help="Optional: SALSA configuration INI file to set up defaults/configurations for software used by SALSA prior to running the pipeline [default value: %default]")
parser.add_option('--no_indexing', default=False, dest='no_indexing', action='store_true', help="Optional: Specify if you want to reconfigure SALSA Configuration files [default value: %default]")

#read in options
(options, args) = parser.parse_args()

#check if INI file exists and then process it
ini_dict = {}
if os.path.isfile(options.salsa_config):
	ini_dict = parse_ini.read_in(options.salsa_config)
else:
	print parser.print_help()
	sys.exit("\n\nError: SALSA configuration INI file does not exist: %s (--salsa_config)\n\n" %(options.salsa_config))

# Reference directory
if options.reference:
	if os.path.isfile(options.reference):
		options.reference = os.path.abspath(options.reference)
	else:
		print parser.print_help()
		sys.exit("\n\nError: FASTA/reference file, %s, doesn't exist! (--reference)\n\n" % (options.reference))
else:
	print parser.print_help()
	sys.exit("\n\nError: Please provide reference file (--reference)\n\n")

#check bed file and set with absolute path
if options.bed:
	if os.path.isfile(options.bed):
		options.bed = os.path.abspath(options.bed)
	else:
		print parser.print_help()
		sys.exit("\n\nError: BED file, %s, doesn't exist! (--bed)\n\n" % (options.bed))
else:
	print parser.print_help()
	sys.exit("\n\nError: Please provide BED file (--bed)\n\n")

#set default transcript and reference file
default_transcripts = scriptdir+"/ensembl_release65_TSCP_fixedWT1.gz"
if ini_dict['transcript_db'] == ".": ini_dict['transcript_db']=default_transcripts

#index reference
if not options.no_indexing:
	print '\n-----------------------------------------'
	print ' Configuring SALSA reference files'
	print '-----------------------------------------\n'
	print 'NOTE: the reference genome is being indexed by BWA and Stampy that will take a while.\n'
	call(['./index_genome.sh',options.reference])


# Make configuration file dirrectory
if not os.path.isdir(scriptdir+"/config_files/"): call(["mkdir", scriptdir+"/config_files"])

# Create CAVA config
generate.cava_configuration(scriptdir+"/templates/cava_config_template", scriptdir+"/config_files/cava_config.txt", options.reference, ini_dict)

# Create CoverView config
generate.coverview_configuration(scriptdir+"/config_files/coverview_config.json", ini_dict)

# Create TOpEx config
generate.topex_configuration(scriptdir+"/config_files/topex_config.ini", ini_dict, options.reference, scriptdir, options.bed)

