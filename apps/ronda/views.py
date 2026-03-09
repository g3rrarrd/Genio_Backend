import random
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import tbl_rondas
from apps.pregunta.models import tbl_preguntas, tbl_pregunta_ronda
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

        if not usuario_id or not categoria_id:
            return Response({"error": "Faltan datos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            categoria = tbl_categoria.objects.get(id_categoria=categoria_id)
            
            nueva_ronda = tbl_rondas.objects.create(
                id_usuarios_id=usuario_id,
                puntaje_total=0.0
            )
        except tbl_categoria.DoesNotExist:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        preguntas_pool = list(tbl_preguntas.objects.filter(id_categoria_id=categoria_id))
        
        if len(preguntas_pool) < 5:
            nueva_ronda.delete()
            return Response({"error": "No hay suficientes preguntas"}, status=status.HTTP_400_BAD_REQUEST)

        preguntas_seleccionadas = random.sample(preguntas_pool, 5)

        for preg in preguntas_seleccionadas:
            tbl_pregunta_ronda.objects.create(
                ronda=nueva_ronda,
                pregunta=preg,
                estado_respuesta=False
            )

        serializer_preguntas = PreguntasSerializer(preguntas_seleccionadas, many=True)

        return Response({
            "ronda_id": nueva_ronda.id_ronda,
            "preguntas": serializer_preguntas.data,
            "puntos_categoria": categoria.puntaje,
            "tiempo_categoria" : categoria.tiempo_limite
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch']) # <-- Usamos PATCH para actualización parcial
    def finalizar(self, request, pk=None):
        ronda = self.get_object()
        puntaje = request.data.get('puntaje_total')
        
        ronda.puntaje_total = puntaje
        ronda.save()
        
        return Response({"status": "Ronda actualizada"}, status=status.HTTP_200_OK)