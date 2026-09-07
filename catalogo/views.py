import json
import os
from django.shortcuts import render
from django.http import Http404
from django.conf import settings

# Documentación: Función auxiliar para cargar los datos desde el archivo JSON
def obtener_productos_json():
    ruta = os.path.join(settings.BASE_DIR, 'catalogo', 'data', 'productos.json')
    if not os.path.exists(ruta):
        return []
    with open(ruta, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

# Documentación: Vista principal con resumen calculado y listado completo de productos[cite: 1]
def lista_productos(request):
    productos = obtener_productos_json()

    # Cálculos dinámicos realizados desde la vista[cite: 1]
    total_productos = len(productos)
    con_stock = sum(1 for p in productos if p['stock'] > 0)
    sin_stock = total_productos - con_stock

    contexto = {
        'productos': productos,
        'total_productos': total_productos,
        'con_stock': con_stock,
        'sin_stock': sin_stock
    }
    return render(request, 'catalogo/lista.html', contexto)

# Documentación: Vista de detalle por ID con manejo de error 404 para casos inexistentes[cite: 1]
def detalle_producto(request, producto_id):
    productos = obtener_productos_json()
    producto = next((p for p in productos if p['id'] == producto_id), None)

    if producto is None:
        raise Http404("El producto no existe en el catálogo.")

    return render(request, 'catalogo/detalle.html', {'producto': producto})