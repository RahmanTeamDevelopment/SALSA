#!env/bin/python

from optparse import OptionParser
from subprocess import call
import os
import sys
from main.version import __version__
from main import generate


def parse_config_file(fn):
	ret = {}
	section = ''
	with open(fn) as infile:
		for line in infile:
			line = line.strip()
			if line == '' or line.startswith('#') or line.startswith(";"): continue
			
			if line[0] == '[' and line[-1] == ']':
				s = line[1:-1]
				if '[' in s or ']' in s or '=' in s: continue
				section = s

			elif line.count('=') == 1:
				key, value = line.split('=')
				key = key.strip()
				value = value.strip()
				if section != '':
					key = '{}.{}'.format(section, key)
				ret[key] = value
	return ret


##############################################################################################################

# Current directory
scriptdir=os.path.dirname(os.path.realpath(__file__))

# Command line argument parsing
parser = OptionParser(description='Configure script for SALSA v{}'.format(__version__), usage='configure_salsa.py <options>', version=__version__)
parser.add_option('--reference', default=None, dest='reference', action='store', help="Required: Input reference file (GRCh37) [default value: %default]")
parser.add_option('--bed', default=None, dest='bed', action='store', help="Required: BED file containing the targeted regions (exons/genes) to use for CoverView/QSM [default value: %default]")
parser.add_option('--salsa_config', default=scriptdir+"/default.ini", dest='salsa_config', action='store', help="Required: SALSA configuration INI file to set up SALSA before running [default value: %default]")
parser.add_option('--no_indexing', default=False, dest='no_indexing', action='store_true', help="Optional: Specify if you want to reconfigure SALSA Configuration files [default value: %default]")


(options, args) = parser.parse_args()
ini_dict = parse_config_file(options.salsa_config)

#set default transcript and reference file
default_transcripts = scriptdir+"/ensembl_release65_TSCP_fixedWT1.gz"
if ini_dict['transcript_db'] == ".": ini_dict['transcript_db']=default_transcripts

# Reference directory
refdir=''
if not options.reference is None:
	ref_with_path=os.path.abspath(options.reference)
else:
	print parser.print_help()
	sys.exit("\n\nError: Please provide reference file (--reference)\n\n")


if not options.no_indexing:
	print '\n-----------------------------------------'
	print ' Configuring SALSA reference files'
	print '-----------------------------------------\n'
	print 'NOTE: the reference genome is being indexed by BWA and Stampy that will take a while.\n'
	call(['./index_genome.sh',ref_with_path])


# Make configuration file dirrectory
if not os.path.isdir(scriptdir+"/config_files/"): call(["mkdir", scriptdir+"/config_files"])

# Create CAVA config
generate.cava_configuration(scriptdir+"/templates/cava_config_template", scriptdir+"/config_files/cava_config.txt", ref_with_path, ini_dict)

# Create CoverView config
generate.coverview_configuration(scriptdir+"/config_files/coverview_config.json", ini_dict)

# Create TOpEx config
generate.topex_configuration(scriptdir+"/config_files/topex_config.ini", ref_with_path, scriptdir, options.bed)


