#!/usr/bin/env bash

set -0 errexit
pip install -r requirement.txt

python manage.py collectstatic --noinput
python mange.py migrate