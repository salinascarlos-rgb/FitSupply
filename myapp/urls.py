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
    path("proveedores/persona/actualizar/<str:id_persona>/", views.actualizar_proveedor_persona, name="actualizar_proveedor_persona"),
    path("proveedores/persona/desactivar/<str:id_persona>/", views.proveedor_desactivar_persona, name="proveedor_desactivar_persona"),
    path("proveedores/persona/reactivar/<str:id_persona>/", views.proveedor_reactivar_persona, name="proveedor_reactivar_persona"),

    # Empresas
    path("proveedores/empresa/actualizar/<str:nit>/", views.actualizar_proveedor_empresa, name="actualizar_proveedor_empresa"),
    path("proveedores/empresa/desactivar/<str:nit>/", views.proveedor_desactivar_empresa, name="proveedor_desactivar_empresa"),
    path("proveedores/empresa/reactivar/<str:nit>/", views.proveedor_reactivar_empresa, name="proveedor_reactivar_empresa"),
    

    # ------------------------
    # Productos
    # ------------------------
    path("productos_menu/", views.productos_menu, name="productos_menu"),
    path("productos/actualizar/<str:codigo>/", views.actualizar_producto, name="actualizar_producto"),
    path("productos/eliminar/<str:codigo>/", views.eliminar_producto, name="eliminar_producto"),

    # ------------------------
    # Clientes
    # ------------------------
    path("clientes/", views.clientes_menu, name="clientes_menu"),
    path("clientes/actualizar/<str:id_cliente>/", views.actualizar_cliente, name="actualizar_cliente"),
    path("clientes/desactivar/<str:id_cliente>/", views.desactivar_cliente, name="desactivar_cliente"),
    path("clientes/activar/<str:id_cliente>/", views.activar_cliente, name="activar_cliente"),

]


