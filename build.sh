#!/usr/bin/env bash

set -e  # Esto habilita el modo de salida inmediata en caso de error
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
