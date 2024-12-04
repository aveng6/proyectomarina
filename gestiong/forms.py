from django import forms
from .models import Empleado





class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'nombre', 'apellido_paterno', 'apellido_materno', 
            'matricula',  
            'situacion', 'area', 'grado'
        ]





 