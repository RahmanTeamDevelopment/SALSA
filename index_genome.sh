#!/bin/bash

message () {
echo; printf '%.0s=' {1..80}; echo
echo "SALSA: $1"
printf '%.0s=' {1..80}; echo; echo
}

ABSOLUTE_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Index genome by BWA
message "Indexing genome by BWA"
${ABSOLUTE_PATH}/tools/bwa-0.7.5a/bwa index -a bwtsw $1; echo

# Create a .fai index
${ABSOLUTE_PATH}/tools/samtools-0.1.19/samtools faidx $1; echo

# Index genome by Stampy
message "Indexing genome by Stampy"
mkdir ${ABSOLUTE_PATH}/index
${ABSOLUTE_PATH}/tools/stampy-1.0.20/stampy.py --species=human --assembly=hg19_ncbi37 -G index/ref $1; echo
${ABSOLUTE_PATH}/tools/stampy-1.0.20/stampy.py -g index/ref -H index/ref; echo


