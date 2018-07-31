#!/bin/bash

message () {
echo; printf '%.0s=' {1..80}; echo
echo "SALSA: $1"
printf '%.0s=' {1..80}; echo; echo
}



unset PYTHONPATH

ABSOLUTE_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIP_ARGS='--no-cache-dir --ignore-installed --force-reinstall'
VERSION="$(python -c "from main.version import __version__; print __version__")"

echo ""
echo "Installing SALSA $VERSION ..."
echo ""


message "Installing CoverView v1.4.3"
cd ${ABSOLUTE_PATH}/tools/
wget https://github.com/RahmanTeamDevelopment/CoverView/archive/v1.4.3.tar.gz
mv v1.4.3.tar.gz CoverView-v1.4.3.tar.gz
tar xvf CoverView-v1.4.3.tar.gz
rm CoverView-v1.4.3.tar.gz
cd CoverView-1.4.3
./install.sh
echo ""


message "Installing CAVA v1.2.3"
cd ${ABSOLUTE_PATH}/tools/Platypus/
./install.sh
echo ""


message "Installing Platypus v0.2.4"
cd ${ABSOLUTE_PATH}/tools/
wget https://github.com/RahmanTeamDevelopment/CoverView/archive/v1.4.3.tar.gz
mv v1.4.3.tar.gz CoverView-v1.4.3.tar.gz
tar xvf CoverView-v1.4.3.tar.gz
rm CoverView-v1.4.3.tar.gz
cd CoverView-1.4.3
./install.sh
echo ""


message "Installing BWA v0.7.5a"
cd ${ABSOLUTE_PATH}/tools/
tar xvjf src/bwa-0.7.5a.tar.bz2
cd bwa-0.7.5a/
make
echo ""


message "Installing samtools 0.1.19"
cd ${ABSOLUTE_PATH}/tools/
tar xvjf src/samtools-0.1.19.tar.bz2
cd samtools-0.1.19/
make
echo ""


message "Installing stampy 1.0.20"
cd ${ABSOLUTE_PATH}/tools/
tar zxvf src/stampy-1.0.20r1642.tgz
cd stampy-1.0.20/
cp makefile makefile.original
sed 's/-Wl//g' makefile.original > makefile
make
echo ""


message "Unpacking Picard"
cd ${ABSOLUTE_PATH}/tools/
unzip src/picard-tools-1.90.zip
mv snappy-java-1.0.3-rc3.jar picard-tools-1.90/


message "Installing R"
cd ${ABSOLUTE_PATH}/tools/
tar zxvf src/R-3.1.2.tar.gz
cd R-3.1.2
./configure
make
make check
echo ""


message "Installing DECoN"
cd ${ABSOLUTE_PATH}/tools/
tar zxvf src/DECoN_Linux_1.0.0.tar.gz
cd DECoN_Linux_1.0.0
mkdir packrat/src/VGAM
cp ${ABSOLUTE_PATH}/tools/src/VGAM_0.9-8.tar.gz packrat/src/VGAM/
[ -w ".Rprofile" ] && rm .Rprofile
${ABSOLUTE_PATH}/tools/R-3.1.2/bin/Rscript sessionInfo.R --bootstrap-packrat > setup.log 2>&1
cp packrat/packrat_source/.Rprofile ./
echo ""


message "Unpacking transcript database"
cd ${ABSOLUTE_PATH}/
unzip tools/src/default_transcripts.zip



### Installing SALSA wraper for the full set of tools
cd ${ABSOLUTE_PATH}

virtualenv -p python2.7 env

source ${ABSOLUTE_PATH}/env/bin/activate

pip install --no-cache-dir --ignore-installed --force-reinstall --upgrade pip
pip install ${PIP_ARGS} -r requirements.txt
pip install -U .

