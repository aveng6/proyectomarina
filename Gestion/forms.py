from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Empleado
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm


class FiltroFechaForm(forms.Form):
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de inicio")
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha de fin")



#Editar Contraseña
class CustomPasswordChangeForm(PasswordChangeForm):
    pass



class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido_paterno', 'apellido_materno',  'matricula', 'cargo', 'area', 'grado']



#Recuperar contraseña
class CustomPasswordResetForm(PasswordResetForm):
    pass



class CustomAuthenticationForm(AuthenticationForm):
    show_password = forms.BooleanField(required=False)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'role', 'password1', 'password2')

        from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Buscar', max_length=100)

