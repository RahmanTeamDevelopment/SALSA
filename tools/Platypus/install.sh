#!/bin/bash

echo ""
echo "Installing Platypus $VERSION ..."
echo ""

unset PYTHONPATH
ABSOLUTE_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIP_ARGS='--no-cache-dir --ignore-installed --force-reinstall'
VERSION="$(python -c "from main.version import __version__; print __version__")"

tar zxvf ${ABSOLUTE_PATH}/../src/Platypus_0.2.4.tgz
mv Platypus_0.4.0/ Platypus_0.2.4

### Installing Platypus
cd ${ABSOLUTE_PATH}

virtualenv -p python2.7 env

source ${ABSOLUTE_PATH}/env/bin/activate

pip install --no-cache-dir --ignore-installed --force-reinstall --upgrade pip
pip install ${PIP_ARGS} -r requirements.txt
pip install -U .

cd Platypus_0.2.4
./buildPlatypus.sh

