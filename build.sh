#!/usr/bin/env bash

<<<<<<< HEAD
set -e  # Habilita el modo de salida inmediata en caso de error

# Instala las dependencias
pip install --no-cache-dir -r requirements.txt

# Ejecuta las tareas de Django
python manage.py collectstatic --noinput
python manage.py migrate
=======
set -0 errexit
pip install -r requirement.txt

python manage.py collectstatic --noinput
python mange.py migrate
>>>>>>> 2c99c4146a9aa150214c13d6e3b25bc59290cb01
