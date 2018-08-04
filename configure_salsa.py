#!env/bin/python

from optparse import OptionParser
from subprocess import call
import os
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
parser.add_option('--reference', default=None, dest='reference', action='store', help="Input reference file (GRCh37) [default value: %default]")
#parser.add_option('--ensembl', default=None, dest='ensembl', action='store', help="Ensembl transcript database")
#parser.add_option('--series', default=None, dest='series', action='store', help="Series code (e.g. CART37A)")
#parser.add_option('--output', default='output', dest='output', action='store', help="Output file name prefix [default value: %default]")
#parser.add_option('--gbk', default=False, dest='gbk', action='store_true', help="Create GBK output [default value: %default]")
#parser.add_option('--ref', default=None, dest='ref', action='store', help="Reference genome file")
#parser.add_option('--annovar', default=False, dest='annovar', action='store_true', help="Create GenePred and FASTA files for Annovar [default value: %default]")
#parser.add_option('--prev_cava_db', default=None, dest='prev_cava_db', action='store', help="CAVA db output of previous run from which CART numbering will be continued")
#parser.add_option('--prev_ref', default=None, dest='prev_ref', action='store', help="Reference genome of previous run from which CART numbering will be continued")
(options, args) = parser.parse_args()


# Reference directory
refdir=''
if not options.reference is None:
	refdir=os.path.abspath(options.reference)
	print refdir
else:
	print parser.print_help()
	sys.exit("\n\nError: Please provide reference file (--reference)\n\n")

# Print welcome message
print '\n-----------------------------------------'
print ' Configuring SALSA reference files'
print '-----------------------------------------\n'
print 'NOTE: the reference genome is being indexed by BWA and Stampy that will take a while.\n'
sys.exit()
call(['./index_genome.sh',refdir])





# Call build_topex.sh script
#print '\n---------------------------------------------------------------------------------'
#print 'Downloading and building components (BWA, Stampy, CoverView, Platypus, CAVA) ...'
#print '---------------------------------------------------------------------------------\n'
#call(['chmod','+x','./build_topex.sh'])
#call(['./build_topex.sh'])

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
