from django.views.generic import TemplateView
from django.shortcuts import render

# Create your views here.


class Index(TemplateView):
    """Este view mostrara la pagina home"""
    template_name = "experiencias/index.html"
