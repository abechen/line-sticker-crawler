#!/bin/sh
export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"
PY_VENV="${APP_HOME}/venv"
REQUIREMENT_FILE="${APP_HOME}/requirements.txt"

pip install virtualenv

mkdir -p ${PY_VENV}

virtualenv -p python2.7 ${PY_VENV}

${PY_VENV}/bin/pip install -r ${REQUIREMENT_FILE}