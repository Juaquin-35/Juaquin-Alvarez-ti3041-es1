from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'), # Detalle por ID,

    # Nuevas rutas de autenticación y transacciones
    path('registro/', views.registrar_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('comprar/<int:producto_id>/', views.realizar_compra, name='realizar_compra'),
    path('admin-panel/', views.panel_admin, name='panel_admin'),

    # Panel Admin Principal
    path('admin-panel/', views.panel_admin, name='panel_admin'),
    
    # Acciones CRUD Admin - Usuarios
    path('admin-panel/usuarios/crear/', views.admin_crear_usuario, name='admin_crear_usuario'),
    path('admin-panel/usuarios/editar/<int:usuario_id>/', views.admin_editar_usuario, name='admin_editar_usuario'),
    path('admin-panel/usuarios/eliminar/<int:usuario_id>/', views.admin_eliminar_usuario, name='admin_eliminar_usuario'),
    
    # Acciones CRUD Admin - Productos & Stock
    path('admin-panel/productos/crear/', views.admin_crear_producto, name='admin_crear_producto'),
    path('admin-panel/productos/stock/<int:producto_id>/', views.admin_actualizar_stock, name='admin_actualizar_stock'),
    path('admin-panel/productos/eliminar/<int:producto_id>/', views.admin_eliminar_producto, name='admin_eliminar_producto'),
]
