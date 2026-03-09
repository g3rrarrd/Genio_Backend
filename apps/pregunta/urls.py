from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PreguntasViewSet

router = DefaultRouter()
router.register(r'', PreguntasViewSet, basename='preguntas')

urlpatterns = [
    path('', include(router.urls)),
]