"""
URL configuration for gestione project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from Gestion import views
from Gestion.views import CustomPasswordResetView, CustomPasswordChangeView, pantalla_principal
from django.views.generic import TemplateView
from Gestion.views import add_element, modify_element, registrar_entrada_salida , delete_element
from django.contrib.auth import views as auth_views
from Gestion.views import search_view
from django.urls import path
from Gestion.views import historial_search_view  
from django.urls import path
from Gestion.views import modify_element









urlpatterns = [



    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  
     path('historial_search/', historial_search_view, name='historial_search'),  # Nombre de la nueva ruta
    path('register/', views.register_view, name='register'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_reset_done/', TemplateView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('pantalla_principal/', pantalla_principal, name='pantalla_principal'),  # Ruta para la pantalla principal
    path('add_element/', add_element, name='add_element'),
     path('registrar_entrada_salida/', registrar_entrada_salida, name='registrar_entrada_salida'),  
     path('delete_element/<int:empleado_id>/', delete_element, name='delete_element'),
     path('gestion-entrada-salida/', views.gestion_entrada_salida, name='gestion_entrada_salida'),
     path('procesar-entrada-salida/', views.procesar_entrada_salida, name='procesar_entrada_salida'),
     path('api/empleado/<str:matricula>/', views.obtener_info_empleado, name='obtener_info_empleado'),
     path('historial-entrada-salida/', views.historial_entrada_salida, name='historial_entrada_salida'),
     path('exportar-historial-excel/', views.exportar_historial_excel, name='exportar_historial_excel'),
     path('redirect_user/', views.redirect_user, name='redirect_user'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.login_view, name='login'),  # Vista de login
    path('pantalla_principal/', views.pantalla_principal, name='pantalla_principal'),  # Vista para Admin
    path('gestion_entrada_salida/', views.gestion_entrada_salida, name='gestion_entrada_salida'),  # Vista para Guardia
    path('historial_entrada_salida/', views.historial_entrada_salida, name='historial_entrada_salida'),  # Vista para Servicios
    path('select_matricula/', views.select_matricula, name='select_matricula'), 
    path('edit_empleado/<str:matricula>/', views.edit_empleado, name='edit_empleado'),
    path('consultar_matricula/', views.consultar_matricula, name='consultar_matricula'), 
    path('edit_empleado/<str:matricula>/', views.edit_empleado, name='edit_empleado'),
path('registro_entrada_salida/', views.registro_entrada_salida, name='registro_entrada_salida'),
path('search/', search_view, name='search'),
    path('change_password/', views.change_password, name='change_password'),
    path('modify_element/<int:empleado_id>/', modify_element, name='modify_element'),



]