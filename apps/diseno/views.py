import time
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import tbl_disenos, tbl_preguntas_diseno
from .serializers import (
    DisenoSerializer,
    PreguntaDisenioSerializer,
    SyncPreguntaSerializer,
    DesignSyncPayloadSerializer,
)


class DisenioViewSet(viewsets.ModelViewSet):
    """
    ViewSet for tbl_disenos. lookup_field = 'code' so URL params are the design code.

    Routes (all under /api/design/):
        POST   /api/design/sync/              → sync full design + questions
        GET    /api/design/{code}/            → retrieve design
        DELETE /api/design/{code}/            → delete design (+ questions cascade)
        GET    /api/design/{code}/questions/  → list questions for a design
        PUT    /api/design/{code}/questions/  → replace questions for a design
    """

    queryset = tbl_disenos.objects.all()
    serializer_class = DisenoSerializer
    lookup_field = 'code'

    # ------------------------------------------------------------------
    # POST /api/design/sync/
    # ------------------------------------------------------------------
    @action(detail=False, methods=['post'], url_path='sync')
    def sync(self, request):
        """
        Accept a DesignSyncPayload from the frontend, upsert the design row,
        and REPLACE all questions (delete-then-insert in a transaction).
        """
        serializer = DesignSyncPayloadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        inner = data['payload']
        code = inner['code']  # already normalised to UPPERCASE
        now_ms = int(time.time() * 1000)

        with transaction.atomic():
            diseno, created = tbl_disenos.objects.get_or_create(
                code=code,
                defaults={'created_at': now_ms},
            )

            diseno.nombre = inner.get('nombre_diseno', diseno.nombre)
            diseno.color_primario = inner.get('color_primario', diseno.color_primario)
            diseno.fuente = inner.get('fuente', diseno.fuente)
            diseno.fondo_url = inner.get('fondo_url_o_base64', diseno.fondo_url)
            diseno.fondo_nombre_archivo = inner.get('fondo_nombre_archivo', diseno.fondo_nombre_archivo)
            diseno.logo_url = inner.get('logo_url_o_base64', diseno.logo_url)
            diseno.logo_nombre_archivo = inner.get('logo_nombre_archivo', diseno.logo_nombre_archivo)
            diseno.fecha_expiracion = inner.get('fecha_expiracion')
            diseno.app_titulo = inner.get('app_titulo', diseno.app_titulo)
            diseno.app_subtitulo = inner.get('app_subtitulo', diseno.app_subtitulo)
            diseno.app_tagline = inner.get('app_tagline', diseno.app_tagline)
            diseno.icono_victoria_url = inner.get('icono_victoria_url', diseno.icono_victoria_url)
            diseno.icono_fallaste_url = inner.get('icono_fallaste_url', diseno.icono_fallaste_url)
            diseno.icono_v_url = inner.get('icono_v_url', diseno.icono_v_url)
            diseno.icono_f_url = inner.get('icono_f_url', diseno.icono_f_url)
            diseno.updated_at = now_ms
            diseno.save()

            # Replace all questions
            tbl_preguntas_diseno.objects.filter(diseno=diseno).delete()

            preguntas_data = inner.get('preguntas', [])
            bulk = [
                tbl_preguntas_diseno(
                    diseno=diseno,
                    pregunta_id=q['id'],
                    pregunta=q['pregunta'],
                    respuesta=q['respuesta'],
                    explicacion=q.get('explicacion', ''),
                    categoria=q.get('categoria', 1),
                )
                for q in preguntas_data
            ]
            tbl_preguntas_diseno.objects.bulk_create(bulk)

        return Response(
            {
                "success": True,
                "code": code,
                "message": "Diseño sincronizado exitosamente.",
                "preguntasGuardadas": len(bulk),
                "timestamp": now_ms,
            },
            status=status.HTTP_200_OK,
        )

    # ------------------------------------------------------------------
    # GET /api/design/{code}/questions/
    # PUT /api/design/{code}/questions/
    # ------------------------------------------------------------------
    @action(detail=True, methods=['get', 'put'], url_path='questions')
    def questions(self, request, code=None):
        code = code.strip().upper()
        try:
            diseno = tbl_disenos.objects.get(code=code)
        except tbl_disenos.DoesNotExist:
            return Response(
                {"success": False, "error": f"Diseño con código '{code}' no encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.method == 'GET':
            qs = tbl_preguntas_diseno.objects.filter(diseno=diseno).order_by('pregunta_id')
            serializer = PreguntaDisenioSerializer(qs, many=True)
            return Response(
                {"success": True, "code": code, "preguntas": serializer.data},
                status=status.HTTP_200_OK,
            )

        # PUT — replace all questions for this design
        serializer = SyncPreguntaSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            tbl_preguntas_diseno.objects.filter(diseno=diseno).delete()
            bulk = [
                tbl_preguntas_diseno(
                    diseno=diseno,
                    pregunta_id=q['id'],
                    pregunta=q['pregunta'],
                    respuesta=q['respuesta'],
                    explicacion=q.get('explicacion', ''),
                    categoria=q.get('categoria', 1),
                )
                for q in serializer.validated_data
            ]
            tbl_preguntas_diseno.objects.bulk_create(bulk)

        diseno.updated_at = int(time.time() * 1000)
        diseno.save(update_fields=['updated_at'])

        return Response(
            {
                "success": True,
                "code": code,
                "preguntasGuardadas": len(bulk),
            },
            status=status.HTTP_200_OK,
        )
