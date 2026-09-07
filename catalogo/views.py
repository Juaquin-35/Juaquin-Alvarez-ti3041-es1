from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# Documentación: Vista de prueba inicial para validar el enrutamiento
def lista_productos(request):
    return HttpResponse("Servidor funcionando. App catalogo activa.")