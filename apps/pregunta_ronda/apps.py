# apps/preguntas/apps.py
from django.apps import AppConfig

class PreguntaRondaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pregunta_ronda'
    label = 'pregunta_ronda'