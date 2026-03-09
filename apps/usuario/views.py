from rest_framework import viewsets, status
from .models import tbl_usuario
from .serializers import UsuariosSerializer
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from apps.ronda.models import tbl_rondas
from apps.ronda.serializers import RondasSerializer
from django.db.models import Sum


class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = tbl_usuario.objects.all()
    serializer_class = UsuariosSerializer

    @action(detail=True, methods=['get'])
    def rondas(self, request, pk=None):
        usuario = self.get_object()
        rondas = tbl_rondas.objects.filter(id_usuarios=usuario)
        serializer = RondasSerializer(rondas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def login_simple(self, request):
        email = request.data.get('email')
        try:
            usuario = tbl_usuario.objects.get(correo=email)
            return Response({
                "id_usuarios": usuario.id_usuarios,
                "identificador": usuario.identificador,
                "correo": usuario.correo
            })
        except tbl_usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=404)
        
    @action(detail=False, methods=['post'])
    def acceso_directo(self, request):
        email = request.data.get('email')
        name = request.data.get('identificador')

        usuario = tbl_usuario.objects.filter(correo=email).first()

        if usuario:
            status_code = 200
        else:
            usuario = tbl_usuario.objects.create(
                correo=email,
                identificador=name,
                descripcion="Jugador de Genio"
            )
            status_code = 201

        return Response({
            "id_usuarios": usuario.id_usuarios,
            "identificador": usuario.identificador,
            "correo": usuario.correo,
            "nuevo_registro": status_code == 201
        }, status=status_code)
    
    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        try:
            usuario = self.get_object()
            usuario.estado = False
            usuario.save()
            return Response({"message": "Cuenta desactivada correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def ranking(self, request):
        try:
            user_id = request.query_params.get('user_id')
            
            top_players = tbl_usuario.objects.filter(estado=True).annotate(
                puntos_acumulados=Sum('rondas__puntaje_total')
            ).order_by('-puntos_acumulados')[:20]
            
            ranking_list = []
            for i, user in enumerate(top_players):
                total_score = user.puntos_acumulados if user.puntos_acumulados else 0
                
                ranking_list.append({
                    "rank": i + 1,
                    "name": user.identificador,
                    "score": total_score,
                    "avatarIcon": "person", 
                    "avatarColor": "#13ec5b"
                })

            # 2. Obtener posición del usuario actual
            user_rank_data = None
            if user_id and user_id not in ['undefined', 'null']:
                try:
                    # Calculamos el puntaje del usuario específico
                    usuario_qs = tbl_usuario.objects.annotate(
                        total=Sum('rondas__puntaje_total')
                    ).get(id_usuarios=user_id)
                    
                    score_actual = usuario_qs.total if usuario_qs.total else 0
                    
                    # Contamos cuántos usuarios tienen una SUMA mayor a la nuestra
                    posicion = tbl_usuario.objects.annotate(
                        total=Sum('rondas__puntaje_total')
                    ).filter(total__gt=score_actual).count() + 1
                    
                    user_rank_data = {
                        "rank": posicion,
                        "name": usuario_qs.identificador,
                        "score": score_actual
                    }
                except tbl_usuario.DoesNotExist:
                    pass

            return Response({
                "top_20": ranking_list,
                "user_rank": user_rank_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Imprime el error en la terminal para que puedas debuguear
            print(f"DEBUG ERROR: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
