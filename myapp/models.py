from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal

# ==========================================
# 👥 MODELOS DE PROVEEDORES
# ==========================================
class ProveedorPersona(models.Model):
    id_persona = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, unique=True)
    productos_suministrados = models.TextField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Proveedor Persona"
        verbose_name_plural = "Proveedores Personas"
        ordering = ["nombre", "primer_apellido"]

    def __str__(self):
        return f"{self.nombre} {self.primer_apellido} {self.segundo_apellido or ''}".strip()


class ProveedorEmpresa(models.Model):
    nit = models.CharField(max_length=20, primary_key=True)
    razon_social = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, unique=True)
    productos_suministrados = models.TextField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Proveedor Empresa"
        verbose_name_plural = "Proveedores Empresas"
        ordering = ["razon_social"]

    def __str__(self):
        return f"{self.razon_social} ({self.nit})"


class Proveedor(models.Model):
    TIPO_CHOICES = [
        ('persona', 'Persona'),
        ('empresa', 'Empresa'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    persona = models.ForeignKey(ProveedorPersona, null=True, blank=True, on_delete=models.CASCADE)
    empresa = models.ForeignKey(ProveedorEmpresa, null=True, blank=True, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        if self.tipo == 'persona' and self.persona:
            return f"{self.persona.nombre} {self.persona.primer_apellido} ({self.persona.id_persona})"
        elif self.tipo == 'empresa' and self.empresa:
            return f"{self.empresa.razon_social} ({self.empresa.nit})"
        return "Proveedor sin asignar"

# ==========================================
# 📦 MODELO DE PRODUCTOS
# ==========================================
class Producto(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True)
    referencia = models.CharField(max_length=100)
    nombre = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

# ==========================================
# 👤 MODELO DE CLIENTES
# ==========================================
class Cliente(models.Model):
    id_cliente = models.CharField(max_length=20, primary_key=True, verbose_name="ID Cliente")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    primer_apellido = models.CharField(max_length=50, verbose_name="Primer Apellido")
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True, verbose_name="Segundo Apellido")
    correo = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=15, unique=True, verbose_name="Teléfono")
    frecuente = models.BooleanField(default=False, verbose_name="Cliente Frecuente")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["id_cliente"]

    def __str__(self):
        return f"{self.id_cliente} - {self.nombre} {self.primer_apellido} {self.segundo_apellido or ''}"

# =========================================
# MODELO: FACTURA DE COMPRA
# =========================================
class FacturaCompra(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("pagada", "Pagada"),
        ("anulada", "Anulada"),
    ]

    numero_factura = models.CharField(max_length=30, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    fecha_emision = models.DateField(default=timezone.now)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    forma_pago = models.CharField(
        max_length=50,
        choices=[
            ("contado", "Contado"),
            ("credito", "Crédito"),
            ("transferencia", "Transferencia"),
            ("efectivo", "Efectivo"),
        ],
        default="contado",
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    observaciones = models.TextField(blank=True, null=True)
    usuario_registro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def calcular_totales(self):
        detalles = self.detalles.all()
        self.subtotal = sum((d.subtotal for d in detalles), Decimal("0.00"))
        self.total_iva = sum((d.iva_monto for d in detalles), Decimal("0.00"))
        self.total = self.subtotal + self.total_iva
        self.save()

    def __str__(self):
        return f"Factura #{self.numero_factura} - {self.proveedor}"


# =========================================
# MODELO: DETALLE DE COMPRA
# =========================================
class DetalleCompra(models.Model):
    factura = models.ForeignKey(FacturaCompra, related_name="detalles", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=16)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    iva_monto = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)
    total_linea = models.DecimalField(max_digits=12, decimal_places=2, editable=False, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        self.iva_monto = (self.subtotal * self.iva_porcentaje) / Decimal("100")
        self.total_linea = self.subtotal + self.iva_monto
        super().save(*args, **kwargs)
        self.factura.calcular_totales() 

# models.py
class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    factura = models.ForeignKey(FacturaCompra, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Nuevo campo
    proveedor = models.ForeignKey('Proveedor', on_delete=models.SET_NULL, null=True, blank=True)

    stock_anterior = models.IntegerField(default=0)
    stock_nuevo = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"

