import random
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import tbl_rondas
from apps.pregunta.models import tbl_preguntas
from apps.pregunta_ronda.models import tbl_pregunta_ronda
from apps.pregunta.serializers import PreguntasSerializer
from .serializers import RondasSerializer
from apps.categoria.models import tbl_categoria

class RondasViewSet(viewsets.ModelViewSet):
    queryset = tbl_rondas.objects.all()
    serializer_class = RondasSerializer

    @action(detail=False, methods=['post'])
    def iniciar_juego(self, request):
        usuario_id = request.data.get('id_usuario')
        categoria_id = request.data.get('id_categoria')
        CANTIDAD_PREGUNTAS = 10  # Definimos la constante aquí

        if not usuario_id or not categoria_id:
            return Response({"error": "Faltan datos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            categoria = tbl_categoria.objects.get(id_categoria=categoria_id)
            
            # 1. Obtenemos las preguntas filtradas por categoría de forma aleatoria directamente
            preguntas_qs = tbl_preguntas.objects.filter(
                id_categoria_id=categoria_id
            ).order_by('?')[:CANTIDAD_PREGUNTAS]

            # 2. Validamos que tengamos las 10 preguntas solicitadas
            if preguntas_qs.count() < CANTIDAD_PREGUNTAS:
                return Response({
                    "error": f"No hay suficientes preguntas en esta categoría. Se requieren {CANTIDAD_PREGUNTAS}."
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. Creamos la ronda una vez validado el pool de preguntas
            nueva_ronda = tbl_rondas.objects.create(
                id_usuarios_id=usuario_id,
                puntaje_total=0.0
            )

            # 4. Registramos la relación en la tabla intermedia
            for preg in preguntas_qs:
                tbl_pregunta_ronda.objects.create(
                    ronda=nueva_ronda,
                    pregunta=preg,
                    estado_respuesta=False
                )

            # 5. Serializamos y retornamos
            serializer_preguntas = PreguntasSerializer(preguntas_qs, many=True)

            return Response({
                "ronda_id": nueva_ronda.id_ronda,
                "preguntas": serializer_preguntas.data,
                "puntos_categoria": categoria.puntaje,
                "tiempo_categoria": categoria.tiempo_limite
            }, status=status.HTTP_201_CREATED)

        except tbl_categoria.DoesNotExist:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def finalizar(self, request, pk=None):
        ronda = self.get_object()
        puntaje = request.data.get('puntaje_total')
        
        ronda.puntaje_total = puntaje
        ronda.save()
        
        return Response({"status": "Ronda actualizada"}, status=status.HTTP_200_OK)