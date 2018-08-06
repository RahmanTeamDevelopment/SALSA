#!/usr/bin/env python

import os
import OptionParser
from subprocess import call
from collections import OrderedDict
from sys import argv
import sys
from main.version import __version__


#def readConfigFile(scriptdir, configpath):
#    ret = OrderedDict()
#    if configpath == None:
#        fn = scriptdir + '/config.txt'
#    else:
#        fn = configpath
#    for line in open(fn):
#        line = line.strip()
#        if line == '': continue
#        if line.startswith('#'): continue
#        if not '=' in line: continue
#        [key, value] = line.split('=')
#        key = key.strip()
#        value = value.strip()
#        ret[key] = value
#    return ret
#
#
#def writeConfigFile(scriptdir, params):
#    out = open(scriptdir + '/config.txt', 'w')
#    for key, value in params.iteritems():
#        out.write(key + ' = ' + value + '\n')
#    out.close()
#
#
#def generateFile(params, fnin, fnout):
#    with open(fnout, "wt") as fout:
#        with open(fnin, "rt") as fin:
#            for line in fin:
#                for key, value in params.iteritems():
#                    line = line.replace('@' + key, value)
#                fout.write(line)

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

scriptdir = os.path.dirname(os.path.realpath(__file__))
workingdir = os.getcwd()

# Command line argument parsing
parser = OptionParser(description='TOpEx (Targeted Optimised Exome) pipeline for SALSA v{}'.format(__version__), usage='salsa TOpEx <options>', version=__version__)
parser.add_option("--output", default=None, dest='output', action='store', help="Required: Output prefix, i.e. Sample name [default value: %default]")
parser.add_option("--fastqs", default=None, dest='fastqs', action='store', help="Required: Comma seperated list of R1 and R2 FASTQ files [default value: %default]")
parser.add_option("--directory", default=workingdir, dest='directory', action='store', help="Optional: Directory to output all files. [default value: %default]")
parser.add_option('--topex_config', default=scriptdir+"/config_files/topex_config.ini", dest='topex_config', action='store', help="Optional: TOpEx configuration INI file to run the pipeline [default value: %default]")

(options, args) = parser.parse_args()

# Checkts to see if the required inputs are provided by the user.
checkInputs(options, parser)

# Welcome message
#print '\n' + '-' * 80
#print 'TOpEx pipeline version ' + __version__
#print '-' * 80 + '\n'
#
# Read configuration file
#params = readConfigFile(scriptdir, options.config)
#
# Additional params
#params['NAME'] = options.name
#params['FASTQ1'], params['FASTQ2'] = options.fastq.split(',')
#params['TOPEXDIR'] = scriptdir
#
#params['MORECV'] = ''
#if not options.full:
#    params['MORECV'] = params['MORECV'] + '-c ' + scriptdir + '/CoverView_default.json'
#else:
#    params['MORECV'] = params['MORECV'] + '-c ' + scriptdir + '/CoverView_full.json'
#if not options.bed is None: params['MORECV'] = params['MORECV'] + ' -b ' + options.bed
#if int(options.threads) > 1: params['MORECV'] = params['MORECV'] + ' -t ' + str(options.threads)
#
#params['MORECAVA'] = ''
#if int(options.threads) > 1: params['MORECAVA'] = params['MORECAVA'] + '-t ' + str(options.threads)
#
#params['MOREPOSTCAVA'] = ''
#if options.all: params['MOREPOSTCAVA'] = '-a '
#
#if options.keep:
#    params['KEEPREMOVE'] = ''
#else:
#    params['KEEPREMOVE'] = 'rm -r ' + params['NAME'] + '_tmp'
#
## Genearate Bash script file
#scriptfn = params['NAME'] + '_topex_pipeline.sh'
#generateFile(params, scriptdir + '/templates/topex_pipeline_template', scriptfn)
#call(['chmod', '+x', scriptfn])
#print 'Bash script has been successfully generated: ' + scriptfn
#
## Run Bash script 
#print '\nRunning the ' + scriptfn + ' script ... '
#call(['./' + scriptfn])
#
## Goodbye message
#print '\n' + '-' * 80
#print 'TOpEx pipeline finished.'
#print '-' * 80 + '\n'
#
