# Generated by Django 5.1.2 on 2024-11-04 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion', '0002_alter_customuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido_paterno', models.CharField(max_length=100)),
                ('apellido_materno', models.CharField(max_length=100)),
                ('curp', models.CharField(max_length=18, unique=True)),
                ('matricula', models.CharField(max_length=100, unique=True)),
                ('cargo', models.CharField(max_length=100)),
                ('area', models.CharField(max_length=100)),
                ('grado', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('hora_entrada', models.TimeField(blank=True, null=True)),
                ('hora_salida', models.TimeField(blank=True, null=True)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gestion.empleado')),
            ],
        ),
    ]
