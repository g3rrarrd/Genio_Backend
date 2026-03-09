from rest_framework import viewsets
from .models import tbl_categoria
from .serializers import CategoriaSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = tbl_categoria.objects.all()
    serializer_class = CategoriaSerializer
