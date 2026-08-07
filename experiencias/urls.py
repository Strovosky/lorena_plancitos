from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import Index, SobreMi, Experiencias_View, Comunidad_View, Aventurero_View, Votacion_View

app_name = "experiencias"

urlpatterns = [
    path("", Index.as_view(), name="home"),
    path("sobre_mi/", SobreMi.as_view(), name='sobre_mi'),
    path("experiencias/", Experiencias_View.as_view(), name='experiencias'),
    path('comunidad/', Comunidad_View.as_view(), name='comunidad'),
    path('aventureros/', Aventurero_View.as_view(), name='aventureros'),
    path('aventureros/votaciones/', Votacion_View.as_view(), name='votaciones')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

