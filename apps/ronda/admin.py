from django.contrib import admin
from .models import tbl_rondas

@admin.register(tbl_rondas)
class RondasAdmin(admin.ModelAdmin):
    list_display = ('id_ronda', 'id_usuarios', 'puntaje_total', 'fecha_jugado')
    readonly_fields = ('fecha_jugado',)