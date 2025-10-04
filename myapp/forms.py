from django import forms
from .models import Producto, ProveedorPersona, ProveedorEmpresa, Cliente


# ------------------------------
# Formulario para Proveedor Persona
# ------------------------------
class ProveedorPersonaForm(forms.ModelForm):
    telefono = forms.RegexField(
        regex=r'^\d{7,15}$',
        error_messages={
            'invalid': "⚠️ El teléfono debe contener solo números (7 a 15 dígitos)."
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 3101234567'
        })
    )

    class Meta:
        model = ProveedorPersona
        fields = [
            'id_persona',
            'nombre',
            'primer_apellido',
            'segundo_apellido',
            'direccion',
            'email',
            'telefono',
            'productos_suministrados'
        ]
        widgets = {
            'id_persona': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Documento de identidad'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre'}),
            'primer_apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primer apellido'}),
            'segundo_apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Segundo apellido (opcional)'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Calle 123 #45-67'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'productos_suministrados': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej: Proteína, creatina, vitaminas...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si la persona ya existe (actualización), deshabilitar id_persona
        if self.instance and self.instance.pk:
            self.fields['id_persona'].disabled = True


# ------------------------------
# Formulario para Proveedor Empresa
# ------------------------------
class ProveedorEmpresaForm(forms.ModelForm):
    telefono = forms.RegexField(
        regex=r'^\d{7,15}$',
        error_messages={
            'invalid': "⚠️ El teléfono debe contener solo números (7 a 15 dígitos)."
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 3101234567'
        })
    )

    class Meta:
        model = ProveedorEmpresa
        fields = [
            'nit',
            'razon_social',
            'direccion',
            'email',
            'telefono',
            'productos_suministrados'
        ]
        widgets = {
            'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIT de la empresa'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razón social'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Calle 123 #45-67'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'productos_suministrados': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej: Proteína, creatina, vitaminas...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si la empresa ya existe (actualización), deshabilitar nit
        if self.instance and self.instance.pk:
            self.fields['nit'].disabled = True

 
# -------------------------------
# Formularios de Producto (nuevos)
# -------------------------------
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

class BuscarProveedorForm(forms.Form):
    query = forms.CharField(
        label="ID Persona o NIT Empresa",
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ingrese ID Persona o NIT Empresa"
        })
    )

# Formulario de Cliente (registrar / actualizar)
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            "id_cliente",
            "nombre",
            "primer_apellido",
            "segundo_apellido",
            "correo",
            "telefono",
            "frecuente",
        ]
        widgets = {
            "id_cliente": forms.TextInput(attrs={"class": "form-control", "placeholder": "ID único del cliente"}),
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre"}),
            "primer_apellido": forms.TextInput(attrs={"class": "form-control", "placeholder": "Primer apellido"}),
            "segundo_apellido": forms.TextInput(attrs={"class": "form-control", "placeholder": "Segundo apellido (opcional)"}),
            "correo": forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@ejemplo.com"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: 3001234567"}),
            "frecuente": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

# Formulario de búsqueda (ID, nombre, apellidos, correo o teléfono)
class BuscarClienteForm(forms.Form):
    busqueda = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Buscar por ID, nombre, apellido, correo o teléfono"}
        ),
    )
