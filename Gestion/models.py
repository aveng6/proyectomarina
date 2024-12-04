from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission




class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    matricula = models.CharField(max_length=100, unique=True)
    cargo = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    grado = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"

class Asistencia(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora_entrada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.empleado} - {self.fecha}"



class CustomUser(AbstractUser):
    role = models.CharField(max_length=30)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)


    # Adding unique related names for groups and permissions to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )



class RegistroEntradaSalida(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    accion = models.CharField(max_length=10)  # 'entrada' o 'salida'
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.empleado} - {self.accion} - {self.fecha_hora}"



ROLES = (
    ('admin', 'Admin'),
    ('guardia', 'Guardia'),
    ('servicios', 'Servicios'),
)

class Usuario(AbstractUser):
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return self.username



class Historial(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    accion = models.CharField(max_length=50)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.empleado} - {self.accion} - {self.fecha_hora}'
