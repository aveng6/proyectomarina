from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from .forms import CustomAuthenticationForm, CustomPasswordChangeForm, CustomUserCreationForm,CustomPasswordResetForm
from .models import CustomUser
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from .forms import CustomPasswordResetForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import EmpleadoForm
from django.http import HttpResponse
from .models import Empleado, RegistroEntradaSalida, Asistencia
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import FiltroFechaForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Historial  
from .forms import SearchForm

def historial_search_view(request):
    form = SearchForm(request.GET or None)
    results = []
    if form.is_valid():
        query = form.cleaned_data.get('query', '')
        results = Historial.objects.filter(
            empleado__nombre__icontains=query
        ) | Historial.objects.filter(
            empleado__apellido_paterno__icontains=query
        ) | Historial.objects.filter(
            empleado__apellido_materno__icontains=query
        )  # Busca en múltiples campos
    return render(request, 'historial_entrada_salida.html', {'form': form, 'historial': results, 'query': query})






def search_view(request):
    query = request.GET.get('query', '')
    results = []
    if query:
        results = Empleado.objects.filter(nombre__icontains=query)  
    return render(request, 'pantalla_principal.html', {'empleados': results, 'query': query})






def gestion_entrada_salida(request):
    message = request.GET.get('message', '')
    message_type = request.GET.get('message_type', '')
    return render(request, 'gestion_entrada_salida.html', {'message': message, 'message_type': message_type})

def procesar_entrada_salida(request):
    if request.method == "POST":
        matricula = request.POST.get('matricula')
        accion = request.POST.get('accion')

        try:
            empleado = Empleado.objects.get(matricula=matricula)
            
            # Obtener el último registro de entrada o salida del empleado
            ultimo_registro = RegistroEntradaSalida.objects.filter(empleado=empleado).order_by('-fecha_hora').first()

            # Validar la acción de entrada/salida según el último registro
            if accion == 'entrada':
                if ultimo_registro and ultimo_registro.accion == 'entrada':
                    return redirect(f'/gestion-entrada-salida/?message=Ya%20has%20registrado%20una%20entrada.%20Registra%20una%20salida%20primero.&message_type=error')
            elif accion == 'salida':
                if not ultimo_registro or ultimo_registro.accion == 'salida':
                    return redirect(f'/gestion-entrada-salida/?message=No%20has%20registrado%20una%20entrada%20previa.%20Registra%20una%20entrada%20primero.&message_type=error')

            # Registrar la entrada o salida
            registro = RegistroEntradaSalida(empleado=empleado, accion=accion)
            registro.save()
            return redirect(f'/gestion-entrada-salida/?message=Registro%20exitoso&message_type=success')
        except Empleado.DoesNotExist:
            return redirect(f'/gestion-entrada-salida/?message=Empleado%20no%20encontrado&message_type=error')
    else:
        return HttpResponse("Método no permitido", status=405)


def registrar_entrada_salida(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        empleado = get_object_or_404(Empleado, matricula=matricula)
        asistencia, created = Asistencia.objects.get_or_create(empleado=empleado, fecha=timezone.now().date())

        if created:
            asistencia.hora_entrada = timezone.now().time()
        else:
            asistencia.hora_salida = timezone.now().time()

        asistencia.save()

        return render(request, 'registrar_entrada_salida.html', {'empleado': empleado, 'asistencia': asistencia})



def registro_entrada_salida(request):
    if request.method == 'POST':
        form = FiltroFechaForm(request.POST)
        if form.is_valid():
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']
            registros = RegistroEntradaSalida.objects.filter(
                fecha_hora__date__gte=fecha_inicio,
                fecha_hora__date__lte=fecha_fin
            ).order_by('-fecha_hora')
        else:
            registros = RegistroEntradaSalida.objects.all().order_by('-fecha_hora')
    else:
        form = FiltroFechaForm()
        registros = RegistroEntradaSalida.objects.all().order_by('-fecha_hora')

    return render(request, 'historial_entrada_salida.html', {'form': form, 'registros': registros})




def obtener_info_empleado(request, matricula):
    try:
        empleado = Empleado.objects.get(matricula=matricula)
        data = {
            'nombre': empleado.nombre,
            'apellido_paterno': empleado.apellido_paterno,
            'apellido_materno': empleado.apellido_materno,
            'cargo': empleado.cargo,
            'area': empleado.area,
            'grado': empleado.grado
        }
        return JsonResponse(data)
    except Empleado.DoesNotExist:
        return JsonResponse({'error': 'Empleado no encontrado'}, status=404)





def select_matricula(request):
    if request.method == 'GET' and 'matricula' in request.GET: 
        matricula = request.GET['matricula'] 
        return redirect('modify_empleado', matricula=matricula) 
    
    empleados = Empleado.objects.all() 
    return render(request, 'select_matricula.html', {'empleados': empleados}) 

def edit_empleado(request, matricula): 
    empleado = get_object_or_404(Empleado, matricula=matricula) 
    is_editing = True 
    
    if request.method == 'POST': 
        form = EmpleadoForm(request.POST, instance=empleado) 
        if form.is_valid(): 
            form.save() 
            return redirect('success_url') 
        else: 
            form = EmpleadoForm(instance=empleado) 
            
        return render(request, 'template_name.html', {'form': form, 'is_editing': is_editing, 'empleado': empleado})








def consultar_matricula(request):
    if request.method == 'GET' and 'matricula' in request.GET:
        matricula = request.GET['matricula']
        return redirect('edit_empleado', matricula=matricula)

    return render(request, 'consultar_matricula.html')

def edit_empleado(request, matricula):
    empleado = get_object_or_404(Empleado, matricula=matricula)
    is_editing = True

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('success_url')
    else:
        form = EmpleadoForm(instance=empleado)

    return render(request, 'select_matricula.html', {'form': form, 'is_editing': is_editing, 'empleado': empleado})










class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'password_change.html'

#Recuperar contraseña
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    email_template_name = 'password_reset_email.html'  # Asegúrate de tener este template
    subject_template_name = 'password_reset_subject.txt'  # Y este también
    success_url = reverse_lazy('password_reset_done')
    template_name = 'password_reset.html'


def create_user_with_role(username, role):
    if role == 'admin':
        password = 'AdminPassword123'
    elif role == 'guardia':
        password = 'GuardiaPassword123'
    elif role == 'servicios':
        password = 'ServiciosPassword123'
    else:
        password = 'DefaultPassword123'

    user = CustomUser.objects.create(
        username=username,
        password=make_password(password),
        role=role
    )

    #Asignar permisos de acuerdo al rol
    if role == 'admin':
        permisos = Permission.objects.all()
        user.user_permissions.set(permisos)
    elif role == 'guardia':
        content_type = ContentType.objects.get_for_model(Usuario)
        permisos = Permission.objects.filter(content_type=content_type, codename__in=['view_usuario'])
        user.user_permissions.set(permisos)
    elif role == 'servicios':
        content_type = ContentType.objects.get_for_model(Usuario)
        permisos = Permission.objects.filter(content_type=content_type, codename__in=['view_usuario'])
        user.user_permissions.set(permisos)

    user.save()
    return user

# views.py
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            role = form.cleaned_data.get('role')
            form.save()  # Guardar el formulario y crear el usuario
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = CustomAuthenticationForm()
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                return redirect('pantalla_principal')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Nombre de usuario o contraseña incorrectos.'})
    return render(request, 'login.html', {'form': form})



#Pantalla Principal
@login_required
def pantalla_principal(request):
    return render(request, 'pantalla_principal.html')




def pantalla_principal(request):
    empleados = Empleado.objects.all() 
    print(f"Rol del usuario: {request.user.rol}")
    return render(request, 'pantalla_principal.html', {'empleados': empleados})



@login_required 
def pantalla_principal_view(request): 
    empleados = Empleado.objects.all() 
    return render(request, 'pantalla_principal.html', {'empleados': empleados})





def add_element(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pantalla_principal')
    else:
        form = EmpleadoForm()
    return render(request, 'add_element.html', {'form': form})




def modify_element(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('pantalla_principal')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'modify_element.html', {'form': form, 'empleado': empleado})





def delete_element(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    empleado.delete()
    return redirect('pantalla_principal')



def historial_entrada_salida(request):
    registros = RegistroEntradaSalida.objects.select_related('empleado').order_by('-fecha_hora')
    return render(request, 'historial_entrada_salida.html', {'registros': registros})


import openpyxl
from django.http import HttpResponse

def exportar_historial_excel(request):
    registros = RegistroEntradaSalida.objects.all().order_by('-fecha_hora')

    # Crear un nuevo libro de trabajo y seleccionar la hoja activa
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Historial de Entrada y Salida"

    # Escribir los encabezados
    headers = ['Nombre', 'Apellido Paterno', 'Apellido Materno', 'Matrícula', 'Acción', 'Fecha y Hora']
    ws.append(headers)

    # Escribir los datos
    for registro in registros:
        ws.append([
            registro.empleado.nombre,
            registro.empleado.apellido_paterno,
            registro.empleado.apellido_materno,
            registro.empleado.matricula,
            registro.accion,
            registro.fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
        ])

    # Crear una respuesta HTTP con el tipo de contenido adecuado
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=historial_entrada_salida.xlsx'

    # Guardar el libro de trabajo en la respuesta
    wb.save(response)
    return response


@login_required
def redirect_user(request):
    if request.user.groups.filter(name='Admin').exists():
        return redirect('pantalla_principal')
    elif request.user.groups.filter(name='Guardia').exists():
        return redirect('gestion_entrada_salida')
    elif request.user.groups.filter(name='Servicios').exists():
        return redirect('historial_entrada_salida')
    else:
        return redirect('login')





@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante, para mantener la sesión activa
            messages.success(request, '¡Tu contraseña ha sido actualizada exitosamente!')
            return redirect('pantalla_principal')  # Redirige a la pantalla principal después de cambiar la contraseña
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})




@login_required
def mi_vista(request):
    contexto = {
        'usuario': request.user,
    }
    return render(request, 'pantalla_principal.html', contexto)



