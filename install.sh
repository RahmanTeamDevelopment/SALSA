#!/bin/bash

unset PYTHONPATH

ABSOLUTE_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIP_ARGS='--no-cache-dir --ignore-installed --force-reinstall'
VERSION="$(python -c "from main.version import __version__; print __version__")"

echo ""
echo "Installing SALSA $VERSION ..."
echo ""


cd ${ABSOLUTE_PATH}/tools/
wget https://github.com/RahmanTeamDevelopment/CoverView/archive/v1.4.3.tar.gz
mv v1.4.3.tar.gz CoverView-v1.4.3.tar.gz
tar xvf CoverView-v1.4.3.tar.gz
rm CoverView-v1.4.3.tar.gz
cd CoverView-1.4.3
./install.sh















### Installing SALSA wraper for the full set of tools
cd ${ABSOLUTE_PATH}

virtualenv -p python2.7 env

source ${ABSOLUTE_PATH}/env/bin/activate

pip install --no-cache-dir --ignore-installed --force-reinstall --upgrade pip
pip install ${PIP_ARGS} -r requirements.txt
pip install -U .

