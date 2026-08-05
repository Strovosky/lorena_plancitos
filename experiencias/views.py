from django.views.generic import TemplateView
from django.shortcuts import render
from .models import Experiencia

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

        
