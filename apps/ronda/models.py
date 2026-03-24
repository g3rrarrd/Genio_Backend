from django.db import models
from apps.usuario.models import tbl_usuario 

class tbl_rondas(models.Model):
    id_ronda = models.AutoField(primary_key=True)
    id_usuarios = models.ForeignKey(tbl_usuario, on_delete=models.CASCADE, related_name='rondas')
    puntaje_total = models.FloatField(default=0.0, blank=False)
    fecha_jugado = models.DateTimeField(auto_now_add=True)
    
    preguntas = models.ManyToManyField('pregunta.tbl_preguntas', through='pregunta.tbl_pregunta_ronda')

    class Meta:
        db_table = 'tbl_rondas'

    def __str__(self):
        return f"Ronda {self.id_ronda} - Usuario {self.id_usuarios}"