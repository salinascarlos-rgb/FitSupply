# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from django.contrib.auth.models import User
from .models import LogAuditoria, Producto, Proveedor, Cliente, FacturaCompra, MovimientoInventario
from .middleware import thread_local


# ------------------------------------------------------------
# Función para obtener el usuario actual desde el middleware
# ------------------------------------------------------------
def get_current_user():
    user = getattr(thread_local, 'user', None)
    if isinstance(user, User) and user.is_authenticated:
        return user
    return None


# ------------------------------------------------------------
# Función genérica para registrar auditorías
# ------------------------------------------------------------
def registrar_auditoria(usuario, modelo, objeto_id, accion, descripcion="", ip=None):
    if not isinstance(usuario, User) or not usuario.is_authenticated:
        usuario = None

    LogAuditoria.objects.create(
        usuario=usuario,
        modelo=modelo,
        objeto_id=objeto_id,
        accion=accion.upper(),
        descripcion=descripcion,
        fecha=timezone.now(),
        ip=ip
    )


# ------------------------------------------------------------
# AUDITORÍA DE FACTURAS (solo al crear)
# ------------------------------------------------------------
@receiver(post_save, sender=FacturaCompra)
def log_factura(sender, instance, created, **kwargs):
    # Solo registrar cuando se crea la factura, no al actualizar totales
    if created:
        registrar_auditoria(
            usuario=getattr(instance, 'usuario_registro', get_current_user()),
            modelo='FacturaCompra',
            objeto_id=instance.pk,
            accion='CREAR',
            descripcion=f"Factura {instance.numero_factura} registrada correctamente"
        )


# ------------------------------------------------------------
# AUDITORÍA DE PRODUCTOS (evita logs por actualización de stock)
# ------------------------------------------------------------
@receiver(post_save, sender=Producto)
def log_producto(sender, instance, created, **kwargs):
    # Evitar registrar cambios automáticos de stock
    if hasattr(instance, "_skip_auditoria") and instance._skip_auditoria:
        return

    accion = 'CREAR' if created else 'ACTUALIZAR'
    registrar_auditoria(
        usuario=get_current_user(),
        modelo='Producto',
        objeto_id=instance.codigo,
        accion=accion,
        descripcion=f"Producto {'creado' if created else 'actualizado'}: {instance.nombre}"
    )


# ------------------------------------------------------------
# AUDITORÍA DE PROVEEDORES
# ------------------------------------------------------------
@receiver(post_save, sender=Proveedor)
def log_proveedor(sender, instance, created, **kwargs):
    accion = 'CREAR' if created else 'ACTUALIZAR'
    registrar_auditoria(
        usuario=get_current_user(),
        modelo='Proveedor',
        objeto_id=instance.pk,
        accion=accion,
        descripcion=f"Proveedor {'creado' if created else 'actualizado'} ({instance.tipo})"
    )


# ------------------------------------------------------------
# AUDITORÍA DE CLIENTES
# ------------------------------------------------------------
@receiver(post_save, sender=Cliente)
def log_cliente(sender, instance, created, **kwargs):
    accion = 'CREAR' if created else 'ACTUALIZAR'
    registrar_auditoria(
        usuario=get_current_user(),
        modelo='Cliente',
        objeto_id=instance.id_cliente,
        accion=accion,
        descripcion=f"Cliente {'registrado' if created else 'modificado'}: {instance.nombre} {instance.primer_apellido}"
    )


# ------------------------------------------------------------
# LOGIN / LOGOUT DE USUARIOS
# ------------------------------------------------------------
@receiver(user_logged_in)
def log_login(sender, user, request, **kwargs):
    registrar_auditoria(
        usuario=user,
        modelo='Usuario',
        objeto_id=user.id,
        accion='LOGIN',
        descripcion=f"Inicio de sesión del usuario {user.username}",
        ip=request.META.get('REMOTE_ADDR')
    )


@receiver(user_logged_out)
def log_logout(sender, user, request, **kwargs):
    registrar_auditoria(
        usuario=user,
        modelo='Usuario',
        objeto_id=user.id,
        accion='LOGOUT',
        descripcion=f"Cierre de sesión del usuario {user.username}",
        ip=request.META.get('REMOTE_ADDR')
    )

