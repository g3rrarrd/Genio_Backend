from rest_framework import serializers
from .models import tbl_categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_categoria
        fields = '__all__'