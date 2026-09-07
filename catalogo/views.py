import json
import os
from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# Documentación: Vista de prueba inicial para validar el enrutamiento
def lista_productos(request):
    return HttpResponse("Servidor funcionando. App catalogo activa.")

# Documentación: Función para cargar los datos desde el archivo JSON
def obtener_productos_json():
    ruta = os.path.join(settings.BASE_DIR, 'catalogo', 'data', 'productos.json')
    if not os.path.exists(ruta):
        return []
    with open(ruta, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

# Documentación: Lista completa de productos
def lista_productos(request):
    productos = obtener_productos_json()
    return render(request, 'catalogo/lista.html', {'productos': productos})

# Documentación: Detalle por id con manejo del caso inexistente (404)
def detalle_producto(request, producto_id):
    productos = obtener_productos_json()
    producto = next((p for p in productos if p['id'] == producto_id), None)

    if producto is None:
        raise Http404("El producto no existe en el catálogo.")

    return render(request, 'catalogo/detalle.html', {'producto': producto})