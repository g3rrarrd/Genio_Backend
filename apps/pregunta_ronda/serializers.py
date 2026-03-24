from rest_framework import serializers

from apps.categoria.models import tbl_categoria
from .models import tbl_pregunta_ronda

class PreguntaRondaSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_pregunta_ronda
        fields = '__all__'