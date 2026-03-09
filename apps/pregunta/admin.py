from django.contrib import admin
from .models import tbl_preguntas, tbl_pregunta_ronda

@admin.register(tbl_preguntas)
class PreguntasAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'id_categoria', 'respuesta_correcta')
    list_filter = ('id_categoria',)
    search_fields = ('pregunta',)

@admin.register(tbl_pregunta_ronda)
class PreguntaRondaAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'ronda', 'estado_respuesta', 'fecha_respondida')