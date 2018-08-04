#!env/bin/python

from optparse import OptionParser
from subprocess import call
import os
import sys
from main.version import __version__


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

# Version
ver = __version__

# Command line argument parsing
descr='Installer script of SALSA '+ver+'.'

parser = OptionParser(description='Configure script for SALSA v{}'.format(__version__), usage='configure_salsa.py <options>', version=__version__)
parser.add_option('--reference', default=None, dest='reference', action='store', help="Required: Input reference file (GRCh37) [default value: %default]")
parser.add_option('--salsa_config', default=None, dest='salsa_config', action='store', help="Required: SALSA configuration INI file to set up SALSA before running [default value: %default]")
parser.add_option('--no_indexing', default=False, dest='no_indexing', action='store_true', help="Optional: Specify if you want to reconfigure SALSA Configuration files [default value: %default]")


(options, args) = parser.parse_args()
ini_dict = parse_config_file(options.salsa_config)

#set default transcript and reference file
default_transcripts = scriptdir+"/ensembl_release65_TSCP_fixedWT1.gz"
if ini_dict['transcript'] == ".": ini_dict['transcript']=default_transcripts

# Reference directory
refdir=''
if not options.reference is None:
	ref_with_path=os.path.abspath(options.reference)
else:
	print parser.print_help()
	sys.exit("\n\nError: Please provide reference file (--reference)\n\n")

#print '\n-----------------------------------------'
#print ' Configuring SALSA reference files'
#print '-----------------------------------------\n'
#print 'NOTE: the reference genome is being indexed by BWA and Stampy that will take a while.\n'
#if not options.no_indexing: call(['./index_genome.sh',ref_with_path])



# Create CAVA config
call(['cp', scriptdir+"/templates/cava_config_template", scriptdir+"/cava_config.txt"])
read_file = open(scriptdir+"/templates/cava_config_template", 'r')
write_file = open(scriptdir+"/cava_config.txt", 'w')
for line in read_file:
	line = line.rstrip()
	if line.startswith("@"):
		if line.startswith("@dbsnp"):
			write_file.write(line+" "+options.cava_dbsnp+"\n")
		elif line.startswith("@target"):
			write_file.write(line+" "+options.cava_target+"\n")
		elif line.startswith("@ensembl"):
			write_file.write(line+" "+options.cava_database+"\n")
		elif line.startswith("@reference"):
			write_file.write(line+" "+ref_with_path+"\n")
		else:
			write_file.write(line+"\n")
	else:
		write_file.write(line+"\n")
read_file.close()
write_file.close()
	



# Create config file
#config=open('config.txt', "wt")
#config.write('ENSTDB = '+scriptdir+'/ensembl_release65_TSCP_fixedWT1.gz\n')
#config.write('CAVA_CONFIG = '+scriptdir+'/cava_config.txt\n')

# CoverView config files
#call(['cp','templates/coverview_config_template','CoverView_default.json'])
#defaultconfig=open('CoverView_default.json', "a")
#defaultconfig.write('\t\"transcript\":  {\"regions\": false, \"profiles\": false, \"poor\": true }\n}\n')
#defaultconfig.close()

# CAVA config file
#call(['cp','templates/cava_config_template','cava_config.txt'])
#cavaconfig=open('cava_config.txt', "a")
#cavaconfig.write('# Name of Ensembl transcript database file\n')
#cavaconfig.write('# Possible values: string | Optional: yes (if not given, no transcript-based annotations are reported)\n')
#cavaconfig.write('@ensembl = '+scriptdir+'/ensembl_release65_TSCP_fixedWT1.gz\n')
#if not options.reference is None: 
#	cavaconfig.write('\n# Name of reference genome file\n')
#	cavaconfig.write('# Possible values: string | Optional: no\n')
#	cavaconfig.write('@reference = '+refdir+'\n')
#cavaconfig.close()

# Call index_genome.sh and add reference fields to config file
#if not options.reference is None: 
#	print '\n------------------------------------'
#	print 'Adding default reference genome ...'
#	print '------------------------------------\n'
#	call(['chmod','+x','./index_genome.sh'])
#	call(['./index_genome.sh',refdir])
#	config.write('REFERENCE = '+refdir+'\n')
#	config.write('GENOME_INDEX = '+scriptdir+'/index/ref\n')
#	config.write('HASH = '+scriptdir+'/index/ref\n')
#else:
#	print '\n-----------------------------------------'
#	print '!!! Referemce genome must be added later.'
#	print '-----------------------------------------'
	
# Close config file and print goodbye message
#config.close()
#print '\n---------------------------------------------------'
#print ' TOPEX PIPELINE v'+ver+' INSTALLATION COMPLETED.'
#if not options.reference is None: print ' Test installation: python test_installation.py'
#print '---------------------------------------------------\n'
