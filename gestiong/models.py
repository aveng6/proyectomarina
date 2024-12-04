from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('guardia', 'Guardia'),
        ('servicios', 'Servicios'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='servicios')
    
    
    contrasena_rol = models.CharField(max_length=128, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='usuario_set',  
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username


# Modelo Empleado

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    matricula = models.CharField(max_length=10)
    situacion = models.CharField(max_length=50, default="Activo")
    area = models.CharField(max_length=100, default="RN-7")
    grado = models.CharField(max_length=50, default="Sin grado")

    


    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

# Modelo RegistroEntradaSalida
class RegistroEntradaSalida(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    hora_entrada = models.DateTimeField()
    hora_salida = models.DateTimeField(null=True, blank=True)
    motivo = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Registro de {self.empleado} - {self.hora_entrada}"












