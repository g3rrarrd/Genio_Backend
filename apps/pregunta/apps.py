# apps/preguntas/apps.py
from django.apps import AppConfig

class PreguntasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pregunta'
    label = 'pregunta'