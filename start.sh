#!/lib/bash
pip3 install pipenv
pipenv install
echo $PWD
pipenv run python3 ./upload_2_pgyer.py
