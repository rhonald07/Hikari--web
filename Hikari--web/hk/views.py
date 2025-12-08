from .utils import validar_datos_registro
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
import hashlib, os, re
import bcrypt



# ==========================================================
# VALIDAR CONTRASEÑA FUERTE
# ==========================================================
def validar_password_fuerte(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[@$!%*?&./_#-]", password):
        return False
    return True


# ==========================================================
# HOME
# ==========================================================
def home_view(request):
    usuario_logeado = "usuario_id" in request.session

    return render(request, "paginas/home.html", {
        "usuario_logeado": usuario_logeado
    })




# ==========================================================
# LOGIN
# ==========================================================
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        # Buscar usuario por correo
        try:
            usuario = Usuario.objects.get(email_usuario=email)
        except Usuario.DoesNotExist:
            messages.error(request, "El correo no está registrado.")
            return render(request, "paginas/login.html")

        # Contraseña ingresada
        entered_password = password.encode("utf-8")

        # Contraseña guardada en base de datos
        stored_password = usuario.contrasena.encode("utf-8")

        # Verificar con bcrypt
        if not bcrypt.checkpw(entered_password, stored_password):
            messages.error(request, "Contraseña incorrecta.")
            return render(request, "paginas/login.html")

        # Guardar sesión usando id_usuario
        request.session["usuario_id"] = usuario.id_usuario

        return redirect("home")

    return render(request, "paginas/login.html")




# ==========================================================
# REGISTRO
# ==========================================================
def registro_view(request):
    if request.method == "POST":

        print(">>> SE EJECUTÓ REGISTRO_VIEW <<<")

        nombre = request.POST.get("nombres")
        apellido = request.POST.get("apellidos")
        identificacion = request.POST.get("identificacion")
        celular = request.POST.get("celular")
        email = request.POST.get("email")
        contrasena = request.POST.get("contrasena")
        confirmar = request.POST.get("confirmar_contrasena")

        # Validar campos vacíos
        if not nombre or not apellido or not email or not contrasena:
            messages.error(request, "Completa todos los campos obligatorios.")
            return redirect("registro")

        # Validar correo
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Correo inválido.")
            return redirect("registro")

        # Validar contraseña mínima
        if len(contrasena) < 6:
            messages.error(request, "La contraseña debe tener al menos 6 caracteres.")
            return redirect("registro")

        # Confirmación
        if contrasena != confirmar:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("registro")

        # Celular de 10 dígitos
        if not re.fullmatch(r"\d{10}", celular):
            messages.error(request, "El celular debe tener 10 dígitos.")
            return redirect("registro")

        # Correo existente
        if Usuario.objects.filter(email_usuario=email).exists():
            messages.error(request, "El correo ya está registrado.")
            return redirect("registro")

        # Encriptar con bcrypt
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(contrasena.encode('utf-8'), salt)

        Usuario.objects.create(
            nombre_usuario=nombre,
            apellido_usuario=apellido,
            email_usuario=email,
            telefono_usuario=celular,
            contrasena=hashed.decode('utf-8'),
            salt=salt.decode('utf-8'),
            rol="usuario"
        )

        messages.success(request, "Cuenta creada exitosamente.")
        return redirect("login")

    return render(request, "paginas/registro.html")




# ==========================================================
# PERFIL
# ==========================================================
def perfil_view(request):
    if "usuario_id" not in request.session:
        return redirect("login")

    usuario = Usuario.objects.get(id_usuario=request.session["usuario_id"])

    return render(request, "paginas/perfil.html", {"usuario": usuario})



# ==========================================================
# CONFIGURACIÓN
# ==========================================================
def configuracion_view(request):
    if "usuario_id" not in request.session:
        return redirect("login")
    return render(request, "paginas/configuracion.html")


# ==========================================================
# DATOS PERSONALES
# ==========================================================
def datos_personales_view(request):
    if "usuario_id" not in request.session:
        return redirect("login")

    usuario = Usuario.objects.get(id_usuario=request.session["usuario_id"])

    if request.method == "POST":

        usuario.nombre_usuario = request.POST.get("nombres")
        usuario.apellido_usuario = request.POST.get("apellidos")
        usuario.telefono_usuario = request.POST.get("telefono")
        usuario.email_usuario = request.POST.get("correo")

        usuario.save()

        messages.success(request, "Datos actualizados correctamente.")
        return redirect("perfil")

    return render(request, "paginas/datos_personales.html", {"usuario": usuario})




# ----------------------------------------
# CRISIS — vista simple por ahora
# ----------------------------------------
def crisis_view(request):
    if "usuario_id" not in request.session:
        return redirect("login")
    return render(request, "paginas/crisis.html")

# ----------------------------------------
# CERRAR SESIÓN
# ----------------------------------------
def logout_view(request):
    request.session.flush()
    return redirect("home")

def error404_view(request):
    return render(request, "paginas/error404.html")

def error500_view(request):
    return render(request, "paginas/error500.html")