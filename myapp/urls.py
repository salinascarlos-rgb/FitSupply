from django.contrib import admin 
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),

    # ------------------------
    # Proveedores
    # ------------------------
    path("proveedores_menu/", views.proveedores_menu, name="proveedores_menu"),

    # Personas
    path('proveedor/actualizar/<int:id>/', views.actualizar_proveedor, name='actualizar_proveedor'),
    path("proveedores/persona/desactivar/<str:id>/", views.proveedor_desactivar, name="proveedor_desactivar"),
    path("proveedores/persona/reactivar/<str:id>/", views.proveedor_reactivar, name="proveedor_reactivar"),

    # ------------------------
    # Productos
    # ------------------------
    path("productos/", views.productos_menu, name="productos_menu"),
    path("productos/actualizar/<str:codigo>/", views.actualizar_producto, name="actualizar_producto"),
    path("productos/desactivar/<str:codigo>/", views.desactivar_producto, name="desactivar_producto"),
    path("productos/activar/<str:codigo>/", views.activar_producto, name="activar_producto"),

    # ------------------------
    # Clientes
    # ------------------------
    path("clientes/", views.clientes_menu, name="clientes_menu"),
    path("clientes/actualizar/<str:id_cliente>/", views.actualizar_cliente, name="actualizar_cliente"),
    path("clientes/desactivar/<str:id_cliente>/", views.desactivar_cliente, name="desactivar_cliente"),
    path("clientes/activar/<str:id_cliente>/", views.activar_cliente, name="activar_cliente"),
    
    # ------------------------
    # Movimientos
    # ------------------------
    path("facturas/", views.facturas_compra, name="facturas_compra"),
    path("factura/<int:pk>/", views.factura_detalle, name="factura_detalle"),
    path("factura/anular/<int:pk>/", views.anular_factura, name="anular_factura"),
    path("movimientos/", views.movimientos_inventario, name="movimientos_inventario"),

    path("auditoria/", views.auditoria_menu, name="auditoria_menu"),
    path("manual/", views.descargar_manual_pdf, name="manual_fitsupply"),




]


