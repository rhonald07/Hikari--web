from django import forms
from .models import Usuario

class RegistroForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ['nombre_usuario','apellido_usuario','email_usuario','telefono_usuario']

class EditarDatosForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario','apellido_usuario','alias','telefono_usuario']

class CambiarContrasenaForm(forms.Form):
    contrasena_actual = forms.CharField(widget=forms.PasswordInput())
    nueva_contrasena = forms.CharField(widget=forms.PasswordInput())
    confirmar_nueva = forms.CharField(widget=forms.PasswordInput())
