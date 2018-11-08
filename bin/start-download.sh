#!/bin/sh
export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"
PY_VENV="${APP_HOME}/venv"

${PY_VENV}/bin/python crawler.py $1