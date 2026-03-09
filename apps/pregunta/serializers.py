from rest_framework import serializers
from .models import tbl_preguntas

class PreguntasSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_preguntas
        fields = [
            'id_pregunta', 
            'pregunta', 
            'respuesta_correcta', 
            'explicacion', 
        ]