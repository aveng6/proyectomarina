#!/usr/bin/env bash

set -e  # Habilita el modo de salida inmediata en caso de error

# Instala las dependencias
pip install --no-cache-dir -r requirements.txt

# Ejecuta las tareas de Django
python manage.py collectstatic --noinput
python manage.py migrate
