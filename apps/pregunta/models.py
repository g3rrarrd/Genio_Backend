from django.db import models
from apps.categoria.models import tbl_categoria 

class tbl_preguntas(models.Model):
    id_pregunta = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey(
        tbl_categoria, 
        on_delete=models.CASCADE, 
        related_name='preguntas'
    )
    codigo = models.CharField(max_length=20, blank=True, default='', db_index=True)
    pregunta = models.TextField(blank=False)
    respuesta_correcta = models.BooleanField(default=False)
    explicacion = models.TextField(blank=True)

    class Meta:
        db_table = 'tbl_preguntas'

    def __str__(self):
        return self.pregunta

