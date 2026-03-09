from django.contrib import admin
from .models import tbl_categoria

@admin.register(tbl_categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id_categoria', 'nombre')
    search_fields = ('nombre_categoria',)