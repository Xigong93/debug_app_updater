#!/bin/sh
pip3 install pipenv
pipenv install
echo $PWD
pipenv run python ./upload.py
