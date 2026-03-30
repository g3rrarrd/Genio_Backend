from django.db import models

class tbl_usuario(models.Model):
    id_usuarios = models.AutoField(primary_key=True)
    identificador = models.CharField(max_length=100, unique=True)
    correo = models.EmailField(max_length=255, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=False, unique=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    permisos = models.BooleanField(default=False)
    codigo_diseno = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        db_table = 'tbl_usuario'