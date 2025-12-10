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
    path('logout/', views.logout_view, name="logout"),
    path('error404/', views.error404_view, name="error404"),
    path('error500/', views.error500_view, name="error500"),

]
