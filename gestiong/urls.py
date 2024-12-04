from django.urls import path
from .views import login_view, generate_report_view
from .views import pantalla_principal
from .views import add_element
from .views import ModifyElementView
from .views import registrar_entrada_salida
from .views import  editar_empleado, eliminar_empleado

urlpatterns = [
    path('', login_view, name='login'),          # Página de inicio de sesión

path('pantalla_principal/', pantalla_principal, name='pantalla_principal'),  # Pantalla del menu
path('add_element/', add_element, name='add_element'),  
path('modify_element/', ModifyElementView.as_view(), name='modify_element'), 
    path('generate_report/', generate_report_view, name='generate_report'),       # Página para generar reporte
 path('registrar/', registrar_entrada_salida, name='registrar_entrada_salida'),
    path('editar_empleado/<int:id>/', editar_empleado, name='editar_empleado'),
    path('eliminar_empleado/<int:id>/', eliminar_empleado, name='eliminar_empleado'),
 
]




   
