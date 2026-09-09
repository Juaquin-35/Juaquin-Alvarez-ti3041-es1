import json
import os
from django.shortcuts import render, redirect
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


# Rutas de los archivos JSON
RUTA_PRODUCTOS = os.path.join(settings.BASE_DIR, 'catalogo', 'data', 'productos.json')
RUTA_USUARIOS = os.path.join(settings.BASE_DIR, 'catalogo', 'data', 'usuarios.json')

# Auxiliares de lectura y escritura
def cargar_json(ruta):
    if not os.path.exists(ruta):
        return []
    with open(ruta, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def guardar_json(ruta, datos):
    with open(ruta, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=2, ensure_ascii=False)


def registrar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuarios = cargar_json(RUTA_USUARIOS)

        # Validar si el usuario ya existe
        if any(u['username'] == username for u in usuarios):
            return render(request, 'catalogo/registro.html', {'error': 'El usuario ya existe.'})

        nuevo_usuario = {
            'id': len(usuarios) + 1,
            'username': username,
            'password': password,
            'rol': 'cliente'
        }
        usuarios.append(nuevo_usuario)
        guardar_json(RUTA_USUARIOS, usuarios)
        return redirect('login')

    return render(request, 'catalogo/registro.html')

def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuarios = cargar_json(RUTA_USUARIOS)

        usuario = next((u for u in usuarios if u['username'] == username and u['password'] == password), None)
        if usuario:
            # Guardar la sesión en el navegador
            request.session['usuario_id'] = usuario['id']
            request.session['username'] = usuario['username']
            request.session['rol'] = usuario['rol']
            return redirect('lista_productos')
        else:
            return render(request, 'catalogo/login.html', {'error': 'Credenciales inválidas.'})

    return render(request, 'catalogo/login.html')

def logout_usuario(request):
    request.session.flush()
    return redirect('lista_productos')


def realizar_compra(request, producto_id):
    # Verificar que el usuario esté autenticado en la sesión
    if 'usuario_id' not in request.session:
        return redirect('login')

    productos = cargar_json(RUTA_PRODUCTOS)
    producto = next((p for p in productos if p['id'] == producto_id), None)

    if not producto:
        raise Http404("El producto no existe.")

    # Regla de negocio: No se puede comprar si el stock es 0
    if producto['stock'] <= 0:
        return render(request, 'catalogo/detalle.html', {
            'producto': producto, 
            'error': 'Producto agotado, no es posible comprar.'
        })

    # Descontar 1 unidad del stock y guardar en el JSON
    producto['stock'] -= 1
    guardar_json(RUTA_PRODUCTOS, productos)

    return render(request, 'catalogo/detalle.html', {
        'producto': producto, 
        'mensaje': '¡Compra realizada con éxito! Se ha reducido el stock.'
    })

def panel_admin(request):
    # Validar permisos de administrador
    if request.session.get('rol') != 'admin':
        return HttpResponseForbidden("Acceso denegado: Se requieren permisos de administrador.")

    # Cargar datos desde los archivos JSON
    productos = cargar_json(RUTA_PRODUCTOS)
    usuarios = cargar_json(RUTA_USUARIOS)

    # Pasar variables al template
    contexto = {
        'productos': productos,
        'usuarios': usuarios
    }
    return render(request, 'catalogo/admin_panel.html', contexto)

# ==========================================
# GESTIÓN DE USUARIOS (PANEL ADMIN)
# ==========================================

def admin_crear_usuario(request):
    if request.session.get('rol') != 'admin':
        return HttpResponseForbidden("Acceso denegado.")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        rol = request.POST.get('rol', 'cliente')

        usuarios = cargar_json(RUTA_USUARIOS)

        if any(u['username'] == username for u in usuarios):
            # Si el usuario existe, podemos redirigir con un parámetro de error o simplemente volver al panel
            return redirect('panel_admin')

        nuevo_id = max([u['id'] for u in usuarios], default=0) + 1
        nuevo_usuario = {
            'id': nuevo_id,
            'username': username,
            'password': password,
            'rol': rol
        }
        usuarios.append(nuevo_usuario)
        guardar_json(RUTA_USUARIOS, usuarios)

    return redirect('panel_admin')


def admin_editar_usuario(request, usuario_id):
    if request.session.get('rol') != 'admin':
        return HttpResponseForbidden("Acceso denegado.")

    if request.method == 'POST':
        rol = request.POST.get('rol')
        password = request.POST.get('password')

        usuarios = cargar_json(RUTA_USUARIOS)
        for u in usuarios:
            if u['id'] == usuario_id:
                u['rol'] = rol
                if password:  # Si se ingresó una nueva clave, se actualiza
                    u['password'] = password
                break
        
        guardar_json(RUTA_USUARIOS, usuarios)

    return redirect('panel_admin')


def admin_eliminar_usuario(request, usuario_id):
    if request.session.get('rol') != 'admin':
        return HttpResponseForbidden("Acceso denegado.")

    if request.method == 'POST':
        usuarios = cargar_json(RUTA_USUARIOS)
        # Evitar que el admin se elimine a sí mismo
        if usuario_id != request.session.get('usuario_id'):
            usuarios = [u for u in usuarios if u['id'] != usuario_id]
            guardar_json(RUTA_USUARIOS, usuarios)

    return redirect('panel_admin')


# ==========================================
# GESTIÓN DE PRODUCTOS (PANEL ADMIN)
# ==========================================

def admin_crear_producto(request):
    if request.session.get('rol') != 'admin':
        return HttpResponseForbidden("Acceso denegado.")

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        categoria = request.POST.get('categoria')
        precio = float(request.POST.get('precio', 0))
        stock = int(request.POST.get('stock', 0))
        imagen = request.POST.get('imagen', '')

        productos = cargar_json(RUTA_PRODUCTOS)
        nuevo_id = max([p['id'] for p in productos], default=0) + 1

        nuevo_producto = {
            'id': nuevo_id,
            'nombre': nombre,
            'categoria': categoria,
            'precio': precio,
            'stock': stock,
            'imagen': imagen
        }
        productos.append(nuevo_producto)
        guardar_json(RUTA_PRODUCTOS, productos)

    return redirect('panel_admin')


def admin_actualizar_stock(request, producto_id):
    if request.session.get('rol') != 'admin':
        return HttpResponseForbidden("Acceso denegado.")

    if request.method == 'POST':
        nuevo_stock = int(request.POST.get('stock', 0))
        productos = cargar_json(RUTA_PRODUCTOS)

        for p in productos:
            if p['id'] == producto_id:
                p['stock'] = max(0, nuevo_stock)  # Evitar stock negativo
                break

        guardar_json(RUTA_PRODUCTOS, productos)

    return redirect('panel_admin')


def admin_eliminar_producto(request, producto_id):
    if request.session.get('rol') != 'admin':
        return HttpResponseForbidden("Acceso denegado.")

    if request.method == 'POST':
        productos = cargar_json(RUTA_PRODUCTOS)
        productos = [p for p in productos if p['id'] != producto_id]
        guardar_json(RUTA_PRODUCTOS, productos)

    return redirect('panel_admin')