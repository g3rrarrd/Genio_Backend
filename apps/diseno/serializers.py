from rest_framework import serializers
from .models import tbl_disenos, tbl_preguntas_diseno


class PreguntaDisenioSerializer(serializers.ModelSerializer):
    """Serializer for tbl_preguntas_diseno — matches the frontend Question interface."""

    id = serializers.IntegerField(source='pregunta_id')

    class Meta:
        model = tbl_preguntas_diseno
        fields = ['id', 'pregunta', 'respuesta', 'explicacion', 'categoria']


class DisenoSerializer(serializers.ModelSerializer):
    preguntas = PreguntaDisenioSerializer(many=True, read_only=True)

    class Meta:
        model = tbl_disenos
        fields = [
            'code',
            'nombre',
            'color_primario',
            'fuente',
            'fondo_nombre_archivo',
            'fondo_url',
            'logo_nombre_archivo',
            'logo_url',
            'fecha_expiracion',
            'app_titulo',
            'app_subtitulo',
            'app_tagline',
            'icono_victoria_url',
            'icono_fallaste_url',
            'icono_v_url',
            'icono_f_url',
            'created_at',
            'updated_at',
            'preguntas',
        ]


# ---------------------------------------------------------------------------
# Serializers for the sync payload (mirrors the TypeScript DesignSyncPayload)
# ---------------------------------------------------------------------------

class SyncPreguntaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    pregunta = serializers.CharField()
    respuesta = serializers.BooleanField()
    explicacion = serializers.CharField(allow_blank=True, default='')
    categoria = serializers.IntegerField(default=1)

    def validate_pregunta(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("pregunta no puede estar vacía.")
        return value.strip()

    def validate_explicacion(self, value):
        if value is None:
            return ''
        return value

    def validate_categoria(self, value):
        if value != 1:
            raise serializers.ValidationError("categoria debe ser 1.")
        return value


class SyncPayloadInnerSerializer(serializers.Serializer):
    code = serializers.CharField()
    nombre_diseno = serializers.CharField(required=False, allow_blank=True, default='')
    color_primario = serializers.CharField(required=False, allow_blank=True, default='')
    fuente = serializers.CharField(required=False, allow_blank=True, default='')
    preguntas = SyncPreguntaSerializer(many=True)
    fondo_url_o_base64 = serializers.CharField(required=False, allow_blank=True, default='')
    fondo_nombre_archivo = serializers.CharField(required=False, allow_blank=True, default='')
    logo_url_o_base64 = serializers.CharField(required=False, allow_blank=True, default='')
    logo_nombre_archivo = serializers.CharField(required=False, allow_blank=True, default='')
    fecha_expiracion = serializers.IntegerField(required=False, allow_null=True, default=None)
    app_titulo = serializers.CharField(required=False, allow_blank=True, default='')
    app_subtitulo = serializers.CharField(required=False, allow_blank=True, default='')
    app_tagline = serializers.CharField(required=False, allow_blank=True, default='')
    icono_victoria_url = serializers.CharField(required=False, allow_blank=True, default='')
    icono_fallaste_url = serializers.CharField(required=False, allow_blank=True, default='')
    icono_v_url = serializers.CharField(required=False, allow_blank=True, default='')
    icono_f_url = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_code(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("code es requerido.")
        return value.strip().upper()


class DesignSyncPayloadSerializer(serializers.Serializer):
    code = serializers.CharField()
    payload = SyncPayloadInnerSerializer()
    queuedAt = serializers.IntegerField(required=False, allow_null=True, default=None)
    status = serializers.CharField(required=False, default='PENDING')

    def validate_code(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("code es requerido.")
        return value.strip().upper()
