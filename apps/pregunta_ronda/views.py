from rest_framework import viewsets
from .models import tbl_pregunta_ronda
from .serializers import PreguntaRondaSerializer

class PreguntaRondaViewSet(viewsets.ModelViewSet):
    queryset = tbl_pregunta_ronda.objects.all()
    serializer_class = PreguntaRondaSerializer
