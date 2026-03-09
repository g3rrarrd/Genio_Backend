from rest_framework import serializers
from .models import tbl_rondas

class RondasSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_rondas
        fields = '__all__'