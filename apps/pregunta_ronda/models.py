from django.db import models

class tbl_pregunta_ronda(models.Model):
    pregunta = models.ForeignKey(
        'pregunta.tbl_preguntas',
        on_delete=models.CASCADE, 
        related_name='rondas_asociadas'
    )
    ronda = models.ForeignKey(
        'ronda.tbl_rondas',
        on_delete=models.CASCADE, 
        related_name='preguntas_asociadas'
    )
    estado_respuesta = models.BooleanField(default=False)
    fecha_respondida = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pregunta', 'ronda')
        db_table = 'tbl_pregunta_ronda'