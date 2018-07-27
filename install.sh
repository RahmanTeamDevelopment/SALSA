#!/bin/bash

unset PYTHONPATH

ABSOLUTE_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIP_ARGS='--no-cache-dir --ignore-installed --force-reinstall'
VERSION="$(python -c "from main.version import __version__; print __version__")"

echo ""
echo "Installing ENSTWriter $VERSION ..."
echo ""

virtualenv -p python2.7 env

source ${ABSOLUTE_PATH}/env/bin/activate

pip install --no-cache-dir --ignore-installed --force-reinstall --upgrade pip
pip install ${PIP_ARGS} -r requirements.txt
pip install -U .

