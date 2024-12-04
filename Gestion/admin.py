from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Registrar el modelo CustomUser usando UserAdmin
admin.site.register(CustomUser, UserAdmin)
