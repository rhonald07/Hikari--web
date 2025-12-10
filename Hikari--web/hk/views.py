from .utils import validar_datos_registro
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
import hashlib, os, re
import bcrypt
from django.utils import timezone
from .models import Usuario, ContactoEmergencia
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, RegistroCrisis
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
import json
from .models import HistorialCrisis, Usuario
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt





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

# ----------------------------------------
# errores
# ----------------------------------------

def error404_view(request):
    return render(request, "paginas/error404.html")

def error500_view(request):
    return render(request, "paginas/error500.html")

# ----------------------------------------
# Cambiar contraseña
# ----------------------------------------

def cambiar_contraseña(request):
    if "usuario_id" not in request.session:
        return redirect("login")

    if request.method == "POST":
        usuario = Usuario.objects.get(id_usuario=request.session["usuario_id"])

        pass_actual = request.POST.get("pass_actual")
        pass_nueva = request.POST.get("pass_nueva")
        pass_confirmar = request.POST.get("pass_confirmar")

        # 1️ Verificar contraseña actual
        if not check_password(pass_actual, usuario.password_usuario):
            messages.error(request, "La contraseña actual no es correcta.")
            return redirect("configuracion")

        # 2️ Verificar que coincidan
        if pass_nueva != pass_confirmar:
            messages.error(request, "Las nuevas contraseñas no coinciden.")
            return redirect("configuracion")

        # 3️ Verificar mínimo 6 caracteres
        if len(pass_nueva) < 6:
            messages.error(request, "La nueva contraseña debe tener al menos 6 caracteres.")
            return redirect("configuracion")

        # 4️ Guardar nueva contraseña (encriptada)
        usuario.password_usuario = make_password(pass_nueva)
        usuario.save()

        messages.success(request, "Tu contraseña ha sido cambiada exitosamente.")
        return redirect("configuracion")

    return redirect("configuracion")



def eliminar_cuenta(request):
    if "usuario_id" not in request.session:
        return redirect("login")

    if request.method == "POST":
        usuario = Usuario.objects.get(id_usuario=request.session["usuario_id"])

        borrar_historial = request.POST.get("borrar_historial")

        # BORRAR HISTORIAL SI ESTÁ MARCADO
        if borrar_historial == "on":
            RegistroCrisis.objects.filter(id_usuario=usuario).delete()

        # ELIMINAR USUARIO
        usuario.delete()

        # Cerrar sesión
        request.session.flush()

        messages.success(request, "Tu cuenta ha sido eliminada correctamente.")
        return redirect("login")

    return redirect("configuracion")

def ejercicio_view(request):
    # Si quieres validar que haya iniciado crisis:
    nivel = request.session.get("nivel_malestar")

    return render(request, "paginas/ejercicio.html", {
        "nivel": nivel,   # por si luego quieres usarlo
    })





def guardar_nivel(request):
    if request.method == "POST":

        try:
            data = json.loads(request.body.decode("utf-8"))
        except:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        nivel = data.get("nivel")
        habilidades = data.get("habilidades", [])

        usuario_id = request.session.get("usuario_id")
        if not usuario_id:
            return JsonResponse({"error": "Usuario no autenticado"}, status=403)

        try:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
        except Usuario.DoesNotExist:
            return JsonResponse({"error": "Usuario no existe"}, status=404)

        HistorialCrisis.objects.create(
            usuario=usuario,
            nivel=nivel,
            habilidades_usadas=json.dumps(habilidades)
        )

        return JsonResponse({"ok": True})

    return JsonResponse({"error": "Método no permitido"}, status=405)



def contactos_emergencia(request):
    if "usuario_id" not in request.session:
        return redirect("login")

    usuario = Usuario.objects.get(id_usuario=request.session["usuario_id"])
    contactos = ContactoEmergencia.objects.filter(usuario=usuario)

    return render(request, "paginas/contactos_emergencia.html", {
        "contactos": contactos
    })



def historial_crisis_view(request):
    usuario_id = request.session.get("usuario_id")
    usuario = Usuario.objects.get(id_usuario=usuario_id)

    historial = HistorialCrisis.objects.filter(usuario=usuario).order_by("-fecha")

    # Convertir habilidades_usadas de JSON → lista
    for h in historial:
        if h.habilidades_usadas:  # si no está vacío
            try:
                h.habilidades_usadas = json.loads(h.habilidades_usadas)
            except:
                h.habilidades_usadas = []
        else:
            h.habilidades_usadas = []

    return render(request, "paginas/historial.html", {"historial": historial})



def eliminar_historial_item(request, id):
    usuario_id = request.session.get("usuario_id")

    item = HistorialCrisis.objects.filter(id=id, usuario_id=usuario_id).first()
    if item:
        item.delete()

    return redirect("historial")


def eliminar_historial_todo(request):
    usuario_id = request.session.get("usuario_id")

    HistorialCrisis.objects.filter(usuario_id=usuario_id).delete()
    return redirect("historial")
