from rest_framework import serializers
from .models import tbl_usuario

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_usuario
        fields = '__all__'