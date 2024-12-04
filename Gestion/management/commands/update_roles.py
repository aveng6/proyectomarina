from django.core.management.base import BaseCommand
from Gestion.models import Usuario  # Asegúrate de usar el nombre correcto de tu aplicación

class Command(BaseCommand):
    help = 'Actualizar roles de usuarios existentes'

    def handle(self, *args, **kwargs):
        # Actualiza los roles de los usuarios
        usuarios_roles = {
            'admin': 'admin',
            'guardia': 'guardia',
            'servicios': 'servicios', 
        }

        for username, rol in usuarios_roles.items():
            try:
                usuario = Usuario.objects.get(username=username)
                usuario.rol = rol
                usuario.save()
                self.stdout.write(self.style.SUCCESS(f'Rol {rol} asignado a {username}'))
            except Usuario.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Usuario {username} no encontrado'))
