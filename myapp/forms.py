from django import forms
from .models import (
    Proveedor, ProveedorPersona, ProveedorEmpresa,
    Producto, Cliente, FacturaCompra, DetalleCompra
)

# =======================================
# 📦 FORMULARIOS DE PRODUCTO
# =======================================
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["codigo", "referencia", "nombre", "categoria", "stock", "precio", "descripcion"]
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. SUP001"}),
            "referencia": forms.TextInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.TextInput(attrs={"class": "form-control"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "precio": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class BuscarProductoForm(forms.Form):
    codigo = forms.CharField(label="Código del producto", max_length=50)

class ActualizarProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["referencia", "nombre", "categoria", "stock", "precio", "descripcion"]
        widgets = {
            "referencia": forms.TextInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.TextInput(attrs={"class": "form-control"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "precio": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

# =======================================
# 👥 FORMULARIOS DE PROVEEDORES
# =======================================
class ProveedorPersonaForm(forms.ModelForm):
    telefono = forms.RegexField(
        regex=r'^\d{7,15}$',
        error_messages={'invalid': "⚠️ El teléfono debe contener solo números (7 a 15 dígitos)."},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3101234567'})
    )

    class Meta:
        model = ProveedorPersona
        fields = [
            'id_persona', 'nombre', 'primer_apellido', 'segundo_apellido',
            'direccion', 'email', 'telefono', 'productos_suministrados'
        ]
        widgets = {
            'id_persona': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Documento de identidad'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'primer_apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'segundo_apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'productos_suministrados': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['id_persona'].disabled = True


class ProveedorEmpresaForm(forms.ModelForm):
    telefono = forms.RegexField(
        regex=r'^\d{7,15}$',
        error_messages={'invalid': "⚠️ El teléfono debe contener solo números (7 a 15 dígitos)."},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3101234567'})
    )

    class Meta:
        model = ProveedorEmpresa
        fields = [
            'nit', 'razon_social', 'direccion', 'email', 'telefono', 'productos_suministrados'
        ]
        widgets = {
            'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIT de la empresa'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razón social'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'productos_suministrados': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['nit'].disabled = True


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['tipo', 'persona', 'empresa', 'activo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'persona': forms.Select(attrs={'class': 'form-select'}),
            'empresa': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BuscarProveedorForm(forms.Form):
    query = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID/NIT o nombre'})
    )

# =======================================
# 🧾 FORMULARIOS DE FACTURA Y DETALLE
# =======================================
class FacturaCompraForm(forms.ModelForm):
    class Meta:
        model = FacturaCompra
        fields = [
            "numero_factura",
            "proveedor",
            "fecha_emision",
            "forma_pago",
            "estado",
            "observaciones",
        ]
        widgets = {
            "numero_factura": forms.TextInput(attrs={"class": "form-control", "placeholder": "Número de factura"}),
            "proveedor": forms.Select(attrs={"class": "form-select"}),
            "fecha_emision": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "forma_pago": forms.Select(attrs={"class": "form-select"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Detalles u observaciones"}),
        }


class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = [
            "producto",
            "cantidad",
            "precio_unitario",
            "iva_porcentaje",
        ]
        widgets = {
            "producto": forms.Select(attrs={"class": "form-select"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "precio_unitario": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "iva_porcentaje": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }


# =======================================
# 👤 FORMULARIOS DE CLIENTE
# =======================================
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "id_cliente", "nombre", "primer_apellido", "segundo_apellido",
            "correo", "telefono", "frecuente"
        ]
        widgets = {
            "id_cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "ID único del cliente"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "primer_apellido": forms.TextInput(attrs={"class": "form-control"}),
            "segundo_apellido": forms.TextInput(attrs={"class": "form-control"}),
            "correo": forms.EmailInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "frecuente": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['id_cliente'].disabled = True


class BuscarClienteForm(forms.Form):
    busqueda = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Buscar por ID, nombre, apellido, correo o teléfono"
        })
    )

