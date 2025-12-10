from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name="registro"),
    path('perfil/', views.perfil_view, name="perfil"),
    path('configuracion/', views.configuracion_view, name="configuracion"),
    path('datos-personales/', views.datos_personales_view, name="datos_personales"),
    path("contacto/agregar/", views.agregar_contacto, name="agregar_contacto"),
    path("contacto/editar/<int:id>/", views.editar_contacto, name="editar_contacto"),
    path("contacto/eliminar/<int:id>/", views.eliminar_contacto, name="eliminar_contacto"),
    path('crisis/', views.crisis_view, name="crisis"),
    path("ejercicio/", views.ejercicio_view, name="ejercicio"),
    path("contactos-emergencia/", views.contactos_emergencia, name="contactos_emergencia"),
    path('logout/', views.logout_view, name="logout"),
    path('error404/', views.error404_view, name="error404"),
    path('error500/', views.error500_view, name="error500"),
    path("cambiar-contraseña/", views.cambiar_contraseña, name="cambiar_contraseña"),
    path("eliminar-cuenta/", views.eliminar_cuenta, name="eliminar_cuenta"),
    path("historial/", views.historial_crisis_view, name="historial"),
    path("historial/eliminar/<int:id>/", views.eliminar_historial_item, name="eliminar_historial_item"),
    path("historial/eliminar-todo/", views.eliminar_historial_todo, name="eliminar_historial_todo"),
    path("guardar-nivel/", views.guardar_nivel, name="guardar_nivel"),

    
    



]
