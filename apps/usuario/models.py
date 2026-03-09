from django.db import models

class tbl_usuario(models.Model):
    id_usuarios = models.AutoField(primary_key=True)
    identificador = models.CharField(max_length=100, unique=True)
    correo = models.EmailField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=False)
    estado = models.BooleanField(default=True)
    emblema = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = '[api_genio].[tbl_usuario]'