from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RondasViewSet

router = DefaultRouter()
router.register(r'', RondasViewSet, basename='rondas')

urlpatterns = [
    path('', include(router.urls)),
]