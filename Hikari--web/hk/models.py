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

    rol = models.CharField(max_length=20, default="usuario")  # ← AGREGAR ESTO

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    usuario_activo = models.BooleanField(default=True)

    metodo_biometrico = models.CharField(
        max_length=20,
        choices=[
            ('ninguno', 'Ninguno'),
            ('huella', 'Huella'),
            ('cara', 'Reconocimiento facial')
        ],
        default='ninguno'
    )

    contrasena = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)

    class Meta:
        db_table = "Usuario"


# ==========================================================
# 2. CONTACTO EMERGENCIA
# ==========================================================
class ContactoEmergencia(models.Model):
    PRIORIDADES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="contactos_emergencia",
        null=True,
        blank=True
    )

    nombre = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    numero = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDADES,
        default='media'
    )

    def __str__(self):
        return f"{self.nombre} ({self.numero}) - {self.prioridad}"


# ==========================================================
# 3. HABILIDAD
# ==========================================================
class Habilidad(models.Model):
    nombre_habilidad = models.CharField(max_length=150)

    modulo = models.CharField(
        max_length=40,
        choices=[
            ('mindfulness', 'Mindfulness'),
            ('tolerancia_malestar', 'Tolerancia al Malestar'),
            ('regulacion_emocional', 'Regulación Emocional'),
            ('efectividad_interpersonal', 'Efectividad Interpersonal')
        ]
    )

    descripcion_habilidad = models.TextField(null=True, blank=True)
    rango_malestar_min = models.IntegerField()
    rango_malestar_max = models.IntegerField()

    imagen_url = models.CharField(max_length=255, null=True, blank=True)
    habilidad_activo = models.BooleanField(default=True)

    class Meta:
        db_table = "Habilidad"

    def __str__(self):
        return self.nombre_habilidad


# ==========================================================
# 4. EJERCICIO
# ==========================================================
class Ejercicio(models.Model):
    id_habilidad = models.ForeignKey(Habilidad, on_delete=models.CASCADE)

    titulo = models.CharField(max_length=200)
    descripcion_ejercicio = models.TextField(null=True, blank=True)
    tipo = models.CharField(
        max_length=20,
        choices=[
            ('lectura', 'Lectura'),
            ('audio', 'Audio'),
            ('visual', 'Visual'),
            ('escrito', 'Escrito')
        ],
        default="lectura"
    )
    duracion_aprox_min = models.IntegerField(null=True, blank=True)
    imagen_url = models.CharField(max_length=255, null=True, blank=True)
    audio_url = models.CharField(max_length=255, null=True, blank=True)

    material_extra = models.JSONField(null=True, blank=True)
    ejercicio_activo = models.BooleanField(default=True)

    class Meta:
        db_table = "Ejercicio"


# ==========================================================
# 5. REGISTRO CRISIS
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


# ==========================================================
# 6. TABLA PUENTE CRISIS - HABILIDAD
# ==========================================================
class CrisisHabilidad(models.Model):
    id_crisis = models.ForeignKey(RegistroCrisis, on_delete=models.CASCADE)
    id_habilidad = models.ForeignKey(Habilidad, on_delete=models.CASCADE)

    ayudo = models.BooleanField(null=True)
    orden_uso = models.IntegerField(null=True)
    comentario = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Crisis_Habilidad"
        unique_together = ('id_crisis', 'id_habilidad')


# ==========================================================
# 7. EMOCIÓN
# ==========================================================
class Emocion(models.Model):
    nombre_emocion = models.CharField(max_length=50)
    persepcion_emocion = models.IntegerField()
    categoria = models.CharField(
        max_length=20,
        choices=[
            ('basica', 'Básica'),
            ('secundaria', 'Secundaria'),
            ('otra', 'Otra')
        ],
        default="basica"
    )

    class Meta:
        db_table = "Emocion"


# ==========================================================
# 8. REGISTRO EMOCIONAL
# ==========================================================
class RegistroEmocional(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_emocion = models.ForeignKey(Emocion, on_delete=models.SET_NULL, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    pensamientos = models.TextField(null=True, blank=True)
    sensaciones = models.TextField(null=True, blank=True)
    contexto = models.TextField(null=True, blank=True)
    registro_sincronizado = models.BooleanField(default=False)

    class Meta:
        db_table = "RegistroEmocional"


# ==========================================================
# 9. PRACTICA HABILIDAD
# ==========================================================
class PracticaHabilidad(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_habilidad = models.ForeignKey(Habilidad, on_delete=models.SET_NULL, null=True)
    id_ejercicio = models.ForeignKey(Ejercicio, on_delete=models.SET_NULL, null=True)

    fecha_practica = models.DateTimeField(auto_now_add=True)
    duracion_practica_segundos = models.IntegerField(null=True, blank=True)

    nota_usuario = models.TextField(null=True, blank=True)
    sincronizado = models.BooleanField(default=False)

    class Meta:
        db_table = "PracticaHabilidad"

class ContactoEmergencia(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="contactos"
    )

    nombre = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    numero = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    prioridad = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[
            ("alta", "Alta"),
            ("media", "Media"),
            ("baja", "Baja"),
        ]
    )

    def __str__(self):
        return f"{self.nombre} - {self.numero} ({self.prioridad})"
