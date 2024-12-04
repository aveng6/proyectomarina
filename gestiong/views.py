import json
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from .forms import EmpleadoForm
from .models import Empleado, RegistroEntradaSalida
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views import View


def add_element(request):
    if request.method == 'POST':
        # Crear una instancia del formulario con los datos del POST
        form = EmpleadoForm(request.POST)

        # Verificar si el formulario es válido
        if form.is_valid():
            form.save()  # Guarda el empleado en la base de datos usando el formulario
            messages.success(request, "Empleado añadido exitosamente.")
            return redirect('pantalla_principal')  # Redirige a la pantalla principal después de guardar
        else:
            # Si el formulario no es válido, puedes imprimir errores
            print(form.errors)  # Esto te ayudará a ver qué campos están fallando

    else:
        form = EmpleadoForm()  # Crea un formulario vacío para la solicitud GET

    return render(request, 'add_element.html', {'form': form})


def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == "POST":
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado editado exitosamente.")
            return redirect('pantalla_principal')
        else:
            print(form.errors)  # Mostrar errores en caso de que el formulario no sea válido
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'editar_empleado.html', {'form': form})


def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == "POST":
        empleado.delete()
        messages.success(request, "Empleado eliminado exitosamente.")
        return redirect('pantalla_principal')
    return render(request, 'eliminar_empleado.html', {'empleado': empleado})


def pantalla_principal(request):
    empleados = Empleado.objects.all()  # Obtener todos los empleados
    return render(request, 'pantalla_principal.html', {'empleados': empleados})


class ModifyElementView(View):
    def get(self, request):
        return render(request, 'modify_element.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect('pantalla_principal')
        else:
            messages.error(request, "Credenciales incorrectas. Inténtalo de nuevo.")

    return render(request, 'login.html')


@csrf_exempt  # Permite solicitudes AJAX sin un token CSRF
def registrar_entrada(request):
    if request.method == "POST":
        data = json.loads(request.body)
        codigo_barra = data.get('codigo_barra')
        try:
            empleado = Empleado.objects.get(curp=codigo_barra)
            RegistroEntradaSalida.objects.create(
                empleado=empleado,
                hora_entrada=timezone.now()
            )
            return JsonResponse({"success": True, "empleado": empleado.nombre})
        except Empleado.DoesNotExist:
            return JsonResponse({"success": False, "error": "Empleado no encontrado"})
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)


def registrar_entrada_salida(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        codigo_barras = request.POST.get('codigo_barras', None)
        curp_manual = request.POST.get('curp_manual', None)

        # Intentar obtener el registro de personal por código de barras o CURP
        if codigo_barras:
            try:
                empleado = Empleado.objects.get(curp=codigo_barras)
            except Empleado.DoesNotExist:
                return render(request, 'registrar_entrada_salida.html', {
                    'error': 'Empleado no encontrado con el código de barras ingresado.'
                })
        elif curp_manual:
            try:
                empleado = Empleado.objects.get(curp=curp_manual)
            except Empleado.DoesNotExist:
                return render(request, 'registrar_entrada_salida.html', {
                    'error': 'Empleado no encontrado con el CURP ingresado.'
                })
        else:
            return render(request, 'registrar_entrada_salida.html', {
                'error': 'Ingrese un código de barras o CURP.'
            })

        # Verificar el último registro para decidir si es entrada o salida
        registro = RegistroEntradaSalida.objects.filter(empleado=empleado).order_by('-id').first()
        if registro and not registro.hora_salida:
            # Registrar salida
            registro.hora_salida = timezone.now()
            registro.save()
            mensaje = 'Salida registrada exitosamente'
        else:
            # Registrar entrada
            RegistroEntradaSalida.objects.create(empleado=empleado, hora_entrada=timezone.now())
            mensaje = 'Entrada registrada exitosamente'

        # Redirigir con un mensaje de éxito a la vista principal
        return render(request, 'pantalla_principal.html', {
            'empleado': empleado,
            'hora_actual': timezone.now(),
            'mensaje': mensaje
        })

    return render(request, 'registrar_entrada_salida.html')


# Vista para generar un reporte
def generate_report_view(request):
    empleados = Empleado.objects.all()  # Obtener todos los empleados
    context = {'empleados': empleados}
    return render(request, 'generate_report.html', context)  # Plantilla para mostrar el reporte
