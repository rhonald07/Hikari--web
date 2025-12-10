from django.db import models


# ==========================================================
# 1. USUARIO
# ==========================================================
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)

    email_usuario = models.CharField(max_length=255, unique=True)
    nombre_usuario = models.CharField(max_length=150)
    apellido_usuario = models.CharField(max_length=150)
    alias = models.CharField(max_length=100, null=True, blank=True)
    telefono_usuario = models.CharField(max_length=30, null=True, blank=True)

    rol = models.CharField(max_length=20, default="usuario")

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    usuario_activo = models.BooleanField(default=True)

    metodo_biometrico = models.CharField(
        max_length=20,
        choices=[('ninguno', 'Ninguno'),
                 ('huella', 'Huella'),
                 ('cara', 'Reconocimiento facial')],
        default='ninguno'
    )

    contrasena = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)

    class Meta:
        db_table = "Usuario"

    def __str__(self):
        return self.alias or self.email_usuario



# ==========================================================
# 2. CONTACTO EMERGENCIA
# (Mantengo solo una versión)
# ==========================================================
class ContactoEmergencia(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="contactos"
    )

    nombre = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=50, null=True, blank=True)
    prioridad = models.CharField(
        max_length=20,
        choices=[("alta", "Alta"), ("media", "Media"), ("baja", "Baja")],
        default="media"
    )

    def __str__(self):
        return f"{self.nombre} - {self.numero} ({self.prioridad})"


# ==========================================================
# 3. HISTORIAL DE CRISIS
# (ARREGLADO y fuera de ContactoEmergencia)
# ==========================================================
class HistorialCrisis(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    nivel = models.IntegerField()
    habilidades_usadas = models.TextField()  # JSON como texto

    def __str__(self):
        return f"{self.usuario.alias} – Nivel {self.nivel} – {self.fecha.strftime('%Y-%m-%d')}"



# ==========================================================
# REGISTRO DE CRISIS
# ==========================================================
class RegistroCrisis(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    nivel_inicial = models.IntegerField()
    nivel_final = models.IntegerField(null=True, blank=True)

    duracion_crisis_segundos = models.IntegerField(null=True, blank=True)
    contacto_emergencia_usado = models.BooleanField(default=False)
    crisis_sincronizado = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "RegistroCrisis"

    def __str__(self):
        return f"Crisis {self.id} (Usuario: {self.id_usuario_id})"
