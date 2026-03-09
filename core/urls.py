from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/usuarios/", include("apps.usuario.urls")),
    path("api/categorias/", include("apps.categoria.urls")),
    path("api/preguntas/", include("apps.pregunta.urls")),
    path("api/rondas/", include("apps.ronda.urls")),
]