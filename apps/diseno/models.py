from django.db import models


class tbl_disenos(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, default='')
    color_primario = models.CharField(max_length=20, blank=True, default='')
    fuente = models.CharField(max_length=100, blank=True, default='')
    fondo_nombre_archivo = models.CharField(max_length=255, blank=True, default='')
    fondo_url = models.TextField(blank=True, default='')
    logo_nombre_archivo = models.CharField(max_length=255, blank=True, default='')
    logo_url = models.TextField(blank=True, default='')
    fecha_expiracion = models.BigIntegerField(null=True, blank=True)
    app_titulo = models.CharField(max_length=200, blank=True, default='')
    app_subtitulo = models.CharField(max_length=200, blank=True, default='')
    app_tagline = models.TextField(blank=True, default='')
    icono_victoria_url = models.TextField(blank=True, default='')
    icono_fallaste_url = models.TextField(blank=True, default='')
    icono_v_url = models.TextField(blank=True, default='')
    icono_f_url = models.TextField(blank=True, default='')
    created_at = models.BigIntegerField(null=True, blank=True)
    updated_at = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_disenos'

    def __str__(self):
        return self.code


class tbl_preguntas_diseno(models.Model):
    diseno = models.ForeignKey(
        tbl_disenos,
        to_field='code',
        on_delete=models.CASCADE,
        related_name='preguntas',
    )
    # Local sequential ID assigned by the frontend within a design
    pregunta_id = models.IntegerField()
    pregunta = models.TextField()
    respuesta = models.BooleanField()
    explicacion = models.TextField()
    categoria = models.IntegerField(default=1)

    class Meta:
        db_table = 'tbl_preguntas_diseno'
        unique_together = ('diseno', 'pregunta_id')

    def __str__(self):
        return f"{self.diseno_id} - Q{self.pregunta_id}"
