from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import tbl_preguntas
from .serializers import PreguntasSerializer, SyncPreguntaSerializer


class PreguntasViewSet(viewsets.ModelViewSet):
    serializer_class = PreguntasSerializer

    def get_queryset(self):
        """
        Supports optional ?codigo=ABC123 query param to filter by design code.
        The code is normalized to UPPERCASE.
        """
        qs = tbl_preguntas.objects.all()
        codigo = self.request.query_params.get('codigo')
        if codigo:
            qs = qs.filter(codigo=codigo.strip().upper())
        return qs

    @action(detail=False, methods=['post'], url_path='sync')
    def sync(self, request):
        """
        POST /api/preguntas/sync/

        Payload esperado:
        {
            "code": "DKPWLA",
            "preguntas": [
                {
                    "id": 1,
                    "pregunta": "...",
                    "respuesta": true,
                    "explicacion": "...",
                    "categoria": 1
                }
            ]
        }

        Reemplaza TODAS las preguntas del código dado (delete + insert).
        """
        code = request.data.get('code', '').strip().upper()
        preguntas_data = request.data.get('preguntas')

        if not code:
            return Response(
                {"error": "El campo 'code' es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(preguntas_data, list):
            return Response(
                {"error": "El campo 'preguntas' debe ser una lista."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SyncPreguntaSerializer(data=preguntas_data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            bulk = [
                tbl_preguntas(
                    pregunta=item['pregunta'],
                    respuesta_correcta=item['respuesta'],
                    explicacion=item.get('explicacion', ''),
                    id_categoria_id=item['categoria'],
                    codigo=code,
                )
                for item in serializer.validated_data
            ]
            created = tbl_preguntas.objects.bulk_create(bulk)

        saved = [
            {
                "id": obj.id_pregunta,
                "codigo": obj.codigo,
                "pregunta": obj.pregunta,
                "respuesta": obj.respuesta_correcta,
                "explicacion": obj.explicacion,
                "categoria": obj.id_categoria_id,
            }
            for obj in created
        ]

        return Response(
            {
                "success": True,
                "code": code,
                "preguntasGuardadas": len(saved),
                "preguntas": saved,
            },
            status=status.HTTP_200_OK,
        )

