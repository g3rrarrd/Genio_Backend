from django.db import models

class tbl_categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=False)
    puntaje = models.FloatField(default=0.0, blank=False)
    tiempo_limite = models.IntegerField(default=10, blank=False)

    class Meta:
        db_table = '[api_genio].[tbl_categoria]'

    def __str__(self):
        return self.nombre