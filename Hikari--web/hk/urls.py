from django.urls import path
from . import views

urlpatterns = [
<<<<<<< Updated upstream
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
=======
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
>>>>>>> Stashed changes
    path('registro/', views.registro_view, name="registro"),
    path('perfil/', views.perfil_view, name="perfil"),
    path('configuracion/', views.configuracion_view, name="configuracion"),
    path('datos-personales/', views.datos_personales_view, name="datos_personales"),
    path('crisis/', views.crisis_view, name="crisis"),
    path('logout/', views.logout_view, name="logout"),

]
