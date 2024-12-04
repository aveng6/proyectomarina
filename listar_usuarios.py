import os
import django

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestione.settings')  # Reemplaza 'tu_proyecto' con el nombre de tu proyecto
django.setup()

from Gestion.models import Usuario  # Reemplaza 'miapp' con el nombre de tu aplicación

# Listar todos los usuarios
usuarios = Usuario.objects.all() 
if usuarios: 
    for usuario in usuarios: 
        print(f"Username: {usuario.username}, Email: {usuario.email}, Rol: {usuario.rol}") 
else: 
    print("No se encontraron usuarios en la base de datos.")