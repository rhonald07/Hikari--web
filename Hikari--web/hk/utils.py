import hashlib, os
import re

def crear_hash_contraseña(contraseña):
    salt = os.urandom(16).hex()  
    hash_result = hashlib.sha256((contraseña + salt).encode()).hexdigest()
    return hash_result, salt

def verificar_contraseña(contraseña_plana, contraseña_hash, salt):
    hash_calculado = hashlib.sha256((contraseña_plana + salt).encode()).hexdigest()
    return hash_calculado == contraseña_hash

def validar_datos_registro(data):
    errores = []

    # ---------- VALIDAR NOMBRE ----------
    if len(data["nombres"].strip()) < 2:
        errores.append("El nombre debe contener al menos 2 caracteres.")

    # ---------- VALIDAR APELLIDO ----------
    if len(data["apellidos"].strip()) < 2:
        errores.append("El apellido debe contener al menos 2 caracteres.")

    # ---------- VALIDAR TELÉFONO ----------
    telefono = data["celular"]
    if not telefono.isdigit() or len(telefono) != 10:
        errores.append("El número de celular debe tener exactamente 10 dígitos.")

    # ---------- VALIDAR CORREO ----------
    correo = data["email"]
    regex_correo = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(regex_correo, correo):
        errores.append("El correo no es válido. Ejemplo: nombre@gmail.com")

    # ---------- VALIDAR CONTRASEÑA ----------
    clave = data["contrasena"]
    if len(clave) < 6:
        errores.append("La contraseña debe tener al menos 6 caracteres.")

    if clave != data["confirmar_contrasena"]:
        errores.append("Las contraseñas no coinciden.")

    return errores