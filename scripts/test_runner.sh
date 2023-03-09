#!/usr/bin/env bash

if [ ! -z $1 ];then
    echo ""
    echo "(i) Only running specified test case: '${1}'"
    echo ""
fi

pipenv install --dev


export PYTHONPATH=`pwd`/app

export ENV_VAR="1"

set -e

pipenv run python -m pytest -vv -s --disable-pytest-warnings ${1}