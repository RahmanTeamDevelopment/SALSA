#!/usr/bin/python

import os
import sys
from optparse import OptionParser
from subprocess import call
from main.version import __version__
import main.parse_ini



def generateFile(params, fnin, fnout):
	with open(fnout, "wt") as fout:
		with open(fnin, "rt") as fin:
			for line in fin:
				for key, value in params.iteritems():
					line = line.replace('@' + key, value)
				fout.write(line)


#this function checks to see if the required options were used when calling the progam
def checkInputs(options, parser):
	if options.fastqs is None:
		print parser.print_help()
		sys.exit('\nError: Input FASTQ files not specified (--fastqs).\n')
	x = options.fastqs.split(',')
	if not len(x) == 2:
		print parser.print_help()
		sys.exit('\nError: Incorrect format for FASTQ files, comma seperated fastq1,fastq2 (--fastqs).\n')
	if not x[0].endswith('.fastq.gz') or not x[1].endswith('.fastq.gz'):
		print parser.print_help()
		sys.exit('\nError: Incorrect format for FASTQ files, each FASTQ file should end with \'.fastq.gz\' (--fastqs).\n')
	if not os.path.isfile(x[0]) or not os.path.isfile(x[1]):
		print parser.print_help()
		sys.exit('\nError: Inputted FASTQ files are not files:\n%s\n%s\n\n' % (x[0], x[1]))
	if options.output is None:
		print parser.print_help()
		sys.exit('\nError: Output file prefix isn\'t specified (--output).\n')
	if not os.path.isdir(options.directory):
		print parser.print_help()
		sys.exit('\nThe specified directory: ' + options.directory + ' does not exist!\n (--directory).\n')
	if not os.access(options.directory, os.W_OK):
		print parser.print_help()
		sys.exit('\nDo not have write premissions to the specified directory (--directory): ' + options.directory + '\n')


##############################################################################################################
##############################################################################################################
#     Things to do:
# 1) create a function to check INI values
# 2) Check CoverView/Platypus/CAVA/postCava parts of the template script
#
##############################################################################################################
##############################################################################################################

def run_topex(arguments):
	scriptdir = os.path.dirname(os.path.realpath(__file__))
	workingdir = os.getcwd()

	# Command line argument parsing
	parser = OptionParser(description='TOpEx (Targeted Optimised Exome) pipeline for SALSA v{}'.format(__version__), usage='salsa TOpEx <options>', version=__version__)
	parser.add_option("--output", default=None, dest='output', action='store', help="Required: Output prefix, i.e. Sample name [default value: %default]")
	parser.add_option("--fastqs", default=None, dest='fastqs', action='store', help="Required: Comma seperated list of R1 and R2 FASTQ files [default value: %default]")
	parser.add_option("--directory", default=workingdir, dest='directory', action='store', help="Optional: Directory to output all files. [default value: %default]")
	parser.add_option('--topex_config', default=scriptdir+"/config_files/topex_config.ini", dest='topex_config', action='store', help="Optional: TOpEx configuration INI file to run the pipeline [default value: %default]")
	parser.add_option('--do_not_run', default=False, dest='do_not_run', action='store_true', help="Optional: Tells SALSA not to run the bash script that TOpEx generates. [default value: %default]")

	(options, args) = parser.parse_args(args=arguments)

	# Checkts to see if the required inputs are provided by the user.
	checkInputs(options, parser)

	#Read in TOpEx INI file
	ini_dict = parse_ini.read_in(options.topex_config)

	params = {}
	params['NAME'] = options.output
	params['OUTPATH'] = options.directory
	#set SALSA directory, which is one directory above the TOpEx script's directory
	params['SALSADIR'] = "/".join(scriptdir.split("/")[:-1])
	params['FASTQ1'], params['FASTQ2'] = options.fastqs.split(',')
	params['REFERENCE'] = ini_dict['reference']
	params['TRANSCRIPTDB'] = ini_dict['transcript_db']
	params['STAMPYINDEX'] = ini_dict['stampy_index']
	params['COVERVIEWCONFIG'] = ini_dict['coverview_json']
	params['COVERVIEWBED'] = ini_dict['coverview_bed']
	params['CAVACONFIG'] = ini_dict['cava_config']
	params['MOREPOSTCAVA'] = ''
	if ini_dict['output_all_variants']: params['MOREPOSTCAVA'] = '-a '
	params['KEEPREMOVE'] = ''
	if not ini_dict['keep_all_files']:
		params['KEEPREMOVE'] = 'rm -rf '+options.output+"_tmp/\nrm "+options.output+".bam\nrm "+options.output+"_sorted.bam"

	# Welcome message
	print '\n' + '-' * 80
	print 'TOpEx pipeline version ' + __version__
	print '-' * 80 + '\n'

	## Genearate Bash script file
	scriptfn = params['NAME'] + '_topex_pipeline.sh'
	generateFile(params, params['SALSADIR']+'/templates/topex_pipeline_template', scriptfn)
	call(['chmod', '+x', scriptfn])
	print 'Bash script has been successfully generated: ' + scriptfn

	# Run Bash script 
	if not options.do_not_run:
		print '\nRunning the ' + scriptfn + ' script ... '	
		call(['./' + scriptfn])

	# Goodbye message
		print '\n' + '-' * 80
		print 'TOpEx pipeline finished.'
		print '-' * 80 + '\n'

