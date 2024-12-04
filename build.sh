#!/usr/bin/env bash

set -e errexit
pip install -r requirement.txt

python manage.py collectstatic --noinput
python manage.py migrate