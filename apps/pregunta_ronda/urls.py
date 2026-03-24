from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PreguntaRondaViewSet

router = DefaultRouter()
router.register(r'', PreguntaRondaViewSet, basename='pregunta_ronda')

urlpatterns = [
    path('', include(router.urls)),
]