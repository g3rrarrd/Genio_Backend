from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuariosViewSet

router = DefaultRouter()
router.register(r'', UsuariosViewSet, basename='usuarios')

urlpatterns = [
    path('', include(router.urls)),
]