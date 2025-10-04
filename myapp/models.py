from django.db import models


class ProveedorPersona(models.Model):
    id_persona = models.CharField(max_length=20, primary_key=True)  # identificación
    nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, unique=True)
    productos_suministrados = models.TextField()

    # Campo para activar/desactivar (soft delete)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.primer_apellido} {self.segundo_apellido or ''}".strip()


class ProveedorEmpresa(models.Model):
    nit = models.CharField(max_length=20, primary_key=True)
    razon_social = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, unique=True)
    productos_suministrados = models.TextField()

    # Campo para activar/desactivar (soft delete)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.razon_social} ({self.nit})"



# -------------------------------
# Modelo de Producto
# -------------------------------
class Producto(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True)  # ID propio
    referencia = models.CharField(max_length=100)
    nombre = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class Cliente(models.Model):
    id_cliente = models.CharField(
        max_length=20,
        primary_key=True,
        verbose_name="ID Cliente"
    )
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    primer_apellido = models.CharField(max_length=50, verbose_name="Primer Apellido")
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True, verbose_name="Segundo Apellido")
    correo = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=15, unique=True, verbose_name="Teléfono")
    frecuente = models.BooleanField(default=False, verbose_name="Cliente Frecuente")

    # 👇 Nuevo campo
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["id_cliente"]

    def __str__(self):
        return f"{self.id_cliente} - {self.nombre} {self.primer_apellido} {self.segundo_apellido or ''}"
