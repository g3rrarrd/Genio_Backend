from rest_framework import serializers
from .models import tbl_preguntas


class PreguntasSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_preguntas
        fields = [
            'id_pregunta',
            'codigo',
            'pregunta',
            'respuesta_correcta',
            'explicacion',
        ]


class SyncPreguntaSerializer(serializers.Serializer):
    """
    Serializer para el payload del frontend.
    Mapeo de campos:
        respuesta  (frontend) -> respuesta_correcta (modelo)
        categoria  (frontend) -> id_categoria       (modelo)
        id         (frontend) -> id_pregunta        (modelo, opcional/numérico)
    """
    id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    codigo = serializers.CharField(required=False, allow_blank=True, default='')
    pregunta = serializers.CharField()
    respuesta = serializers.BooleanField()
    explicacion = serializers.CharField(allow_blank=True, default='')
    categoria = serializers.IntegerField()

    def validate_categoria(self, value):
        from apps.categoria.models import tbl_categoria
        if not tbl_categoria.objects.filter(id_categoria=value).exists():
            raise serializers.ValidationError(
                f"La categoría con id={value} no existe."
            )
        return value