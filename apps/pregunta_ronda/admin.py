from django.contrib import admin
from .models import tbl_pregunta_ronda

@admin.register(tbl_pregunta_ronda)
class PreguntaRondaAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'ronda', 'estado_respuesta', 'fecha_respondida')