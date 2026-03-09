from rest_framework import viewsets
from .models import tbl_preguntas
from .serializers import PreguntasSerializer

class PreguntasViewSet(viewsets.ModelViewSet):
    queryset = tbl_preguntas.objects.all()
    serializer_class = PreguntasSerializer
    