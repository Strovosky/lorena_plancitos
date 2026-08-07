from django.views.generic import TemplateView, ListView
from django.shortcuts import render
from .models import Experiencia
from aventurero.models import Aventurero

# Create your views here.

app_name = 'experiencias'

class Index(TemplateView):
    """Este view mostrara la pagina index"""
    template_name = "experiencias/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiencias'] = Experiencia.objects.all()[:3]
        context['experiencia_estrella'] = Experiencia.objects.first()
        return context

class SobreMi(TemplateView):
    """Este view montrará la pagina sobre_mi"""
    template_name = 'experiencias/sobre_mi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["experiencias"] = Experiencia.objects.all()[:5]
        return context

class Experiencias_View(ListView):
    "Este view mostrara la pagina experiencias"

    template_name = 'experiencias/experiencias.html'
    model = Experiencia

class Comunidad_View(ListView):
    "Este view mostrará la página comunidad"

    template_name = 'experiencias/comunidad.html'
    model = Experiencia

class Aventurero_View(ListView):
    "Esta vista mostrará los aventureros registrados"

    template_name = 'experiencias/aventureros.html'
    model = Aventurero

class Votacion_View(ListView):
    "Esta vista mostrará la pagina donde se votara por un aventurero."

    template_name = 'experiencias/votaciones.html'
    model = Aventurero
        
