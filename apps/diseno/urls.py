from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisenioViewSet

router = DefaultRouter()
router.register(r'', DisenioViewSet, basename='diseno')

urlpatterns = [
    path('', include(router.urls)),
]
