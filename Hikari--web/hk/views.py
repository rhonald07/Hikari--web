from .utils import validar_datos_registro
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
import hashlib, os, re
import bcrypt
from django.utils import timezone
from .models import Usuario, ContactoEmergencia
from django.shortcuts import render, redirect, get_object_or_404






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
    usuario_id = request.session.get("usuario_id")
    alias = request.session.get("usuario_alias")

    context = {
        "usuario_logeado": bool(usuario_id),  # para los IF del home
        "alias": alias,                       # para el mensaje de bienvenida
    }
    return render(request, "paginas/home.html", context)





# ==========================================================
# LOGIN
# ==========================================================
def login_view(request):
    if request.method == "POST":
        correo = request.POST.get("correo")
        password = request.POST.get("password")

        if not correo or not password:
            messages.error(request, "Correo y contraseña son obligatorios.")
            return redirect("login")

        try:
            usuario = Usuario.objects.get(email_usuario=correo)
        except Usuario.DoesNotExist:
            messages.error(request, "Correo o contraseña incorrectos.")
            return redirect("login")

        # Verificar contraseña
        if bcrypt.checkpw(password.encode("utf-8"), usuario.contrasena.encode("utf-8")):
            request.session["usuario_id"] = usuario.id_usuario
            request.session["usuario_alias"] = usuario.alias
            return redirect("home")
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
            return redirect("login")

    return render(request, "paginas/login.html")








# ==========================================================
# REGISTRO
# ==========================================================
def registro_view(request):
    if request.method == "POST":

        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        alias = request.POST.get("alias")
        correo = request.POST.get("correo")
        telefono = request.POST.get("telefono")
        password = request.POST.get("password")

        # Validar campos básicos
        if not correo or not password:
            messages.error(request, "Correo y contraseña son obligatorios.")
            return redirect("registro")

        # Validar si ya existe el correo
        if Usuario.objects.filter(email_usuario=correo).exists():
            messages.error(request, "Este correo ya está registrado.")
            return redirect("registro")

        # Crear usuario vacío primero
        usuario = Usuario.objects.create(
            nombre_usuario=nombres,
            apellido_usuario=apellidos,
            alias=alias,
            email_usuario=correo,
            telefono_usuario=telefono,
            rol="usuario",
            usuario_activo=True,
            fecha_creacion=timezone.now(),
        )

        # Generar hash y salt correctamente
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)

        usuario.contrasena = hashed.decode('utf-8')
        usuario.salt = salt.decode('utf-8')
        usuario.save()

        messages.success(request, "Cuenta creada con éxito. Ahora inicia sesión.")
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
    contactos = ContactoEmergencia.objects.filter(usuario=usuario)

    if request.method == "POST":

        # ---------------------------------------------------
        # 1️⃣ AGREGAR CONTACTO NUEVO
        # ---------------------------------------------------
        if request.POST.get("accion") == "agregar_contacto":

            nuevo_nombre = request.POST.get("nuevo_nombre")
            nuevo_numero = request.POST.get("nuevo_numero")
            nuevo_prioridad = request.POST.get("nuevo_prioridad")

            if nuevo_nombre and nuevo_numero:
                ContactoEmergencia.objects.create(
                    usuario=usuario,
                    nombre=nuevo_nombre,
                    numero=nuevo_numero,
                    prioridad=nuevo_prioridad
                )
                messages.success(request, "Contacto agregado correctamente.")
            else:
                messages.error(request, "Debes llenar nombre y número para agregar un contacto.")

            return redirect("datos_personales")

        # ---------------------------------------------------
        # 2️⃣ GUARDAR DATOS PERSONALES
        # Solo se ejecuta si el POST contiene "correo"
        # ---------------------------------------------------
        if request.POST.get("correo"):

            usuario.nombre_usuario = request.POST.get("nombres")
            usuario.apellido_usuario = request.POST.get("apellidos")
            usuario.alias = request.POST.get("alias")
            usuario.telefono_usuario = request.POST.get("telefono")
            usuario.email_usuario = request.POST.get("correo")

            usuario.save()
            request.session["usuario_alias"] = usuario.alias

        # ---------------------------------------------------
        # 3️⃣ EDITAR CONTACTOS EXISTENTES
        # ---------------------------------------------------
        for contacto in contactos:
            nombre = request.POST.get(f"nombre_{contacto.id}")
            numero = request.POST.get(f"numero_{contacto.id}")
            prioridad = request.POST.get(f"prioridad_{contacto.id}")

            if nombre:
                contacto.nombre = nombre
            if numero:
                contacto.numero = numero
            if prioridad:
                contacto.prioridad = prioridad

            contacto.save()

        messages.success(request, "Datos actualizados correctamente.")
        return redirect("datos_personales")

    return render(request, "paginas/datos_personales.html", {
        "usuario": usuario,
        "contactos": contactos,
    })





def agregar_contacto(request):
    if "usuario_id" not in request.session:
        return redirect("login")

    usuario = Usuario.objects.get(id_usuario=request.session["usuario_id"])

    if request.method == "POST":
        ContactoEmergencia.objects.create(
            usuario=usuario,
            nombre=request.POST.get("nombre"),
            numero=request.POST.get("numero"),
            prioridad=request.POST.get("prioridad")
        )

    return redirect("datos_personales")



def editar_contacto(request, id):
    if "usuario_id" not in request.session:
        return redirect("login")

    contacto = get_object_or_404(ContactoEmergencia, id=id)

    # Aseguramos que el contacto pertenece al usuario logueado
    if contacto.usuario_id != request.session["usuario_id"]:
        messages.error(request, "No tienes permiso para editar este contacto.")
        return redirect("datos_personales")

    if request.method == "POST":
        contacto.nombre = request.POST.get("nombre")
        contacto.numero = request.POST.get("numero")
        contacto.prioridad = request.POST.get("prioridad")
        contacto.save()

        messages.success(request, "Contacto actualizado correctamente.")
        return redirect("datos_personales")

    return render(request, "paginas/editar_contacto.html", {
        "contacto": contacto
    })

def eliminar_contacto(request, id):
    if "usuario_id" not in request.session:
        return redirect("login")

    # Buscar el contacto o mostrar error 404 si no existe
    contacto = get_object_or_404(ContactoEmergencia, id=id)

    # Revisar que el contacto sí pertenece al usuario logueado
    if contacto.usuario_id != request.session["usuario_id"]:
        messages.error(request, "No tienes permiso para eliminar este contacto.")
        return redirect("datos_personales")

    # Eliminar contacto
    contacto.delete()
    messages.success(request, "Contacto eliminado correctamente.")

    return redirect("datos_personales")







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