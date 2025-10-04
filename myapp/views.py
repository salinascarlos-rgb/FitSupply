from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProveedorPersonaForm,ProveedorEmpresaForm,ProveedorPersonaForm, ProveedorEmpresaForm, ProductoForm, BuscarProductoForm, ActualizarProductoForm, BuscarProveedorForm, ClienteForm, BuscarClienteForm
from .models import ProveedorPersona, ProveedorEmpresa, Producto, Cliente

# Create your views here.


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        # 1. Validación de campos vacíos
        if not username or not password1 or not password2:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": "Debe llenar todos los campos antes de continuar"
            })

        # 2. Validación de coincidencia de contraseñas
        if password1 != password2:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": "Las contraseñas no coinciden"
            })

        # 3. Validación de longitud mínima de contraseña
        if len(password1) < 8:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": "La contraseña debe tener al menos 8 caracteres"
            })

        # 4. Intentar crear usuario
        try:
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            login(request, user)
            return redirect('tasks')
        except IntegrityError:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": "Este usuario ya existe, elija otro nombre de usuario"
            })

@login_required   
def tasks(request):
    return render(request, 'tasks.html')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Por favor ingresa usuario y contraseña'
            })

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('tasks')
        
# -------------------------------
# Vista Productos
# -------------------------------
@login_required
def productos_menu(request):
    opcion = request.GET.get("opcion", "registrar")
    mensaje = None
    resultado = None

    # Registrar producto
    if opcion == "registrar":
        if request.method == "POST":
            form_registrar = ProductoForm(request.POST)
            if form_registrar.is_valid():
                form_registrar.save()
                mensaje = "✅ Producto registrado con éxito."
                form_registrar = ProductoForm()  # resetear formulario
        else:
            form_registrar = ProductoForm()
        form_buscar = BuscarProductoForm()

    # Buscar producto
    elif opcion == "buscar":
        form_registrar = ProductoForm()
        if request.method == "POST":
            form_buscar = BuscarProductoForm(request.POST)
            if form_buscar.is_valid():
                codigo = form_buscar.cleaned_data["codigo"]
                try:
                    resultado = Producto.objects.get(codigo=codigo)
                except Producto.DoesNotExist:
                    mensaje = "⚠️ No se encontró un producto con ese código."
            else:
                mensaje = "⚠️ Código inválido."
        else:
            form_buscar = BuscarProductoForm()

    # Lista de productos
    productos = Producto.objects.all().order_by("codigo")

    return render(request, "productos_menu.html", {
        "opcion": opcion,
        "form_registrar": form_registrar,
        "form_buscar": form_buscar,
        "resultado": resultado,
        "mensaje": mensaje,
        "productos": productos
    })


@login_required
def actualizar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)

    if request.method == "POST":
        form = ActualizarProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Producto actualizado con éxito.")
            return redirect("productos_menu")
        else:
            messages.error(request, "⚠️ Corrige los errores en el formulario.")
    else:
        form = ActualizarProductoForm(instance=producto)

    return render(request, "actualizar_producto.html", {
        "form": form,
        "producto": producto
    })


@login_required
def eliminar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)

    if request.method == "POST":
        producto.delete()
        messages.success(request, "✅ Producto eliminado con éxito.")
        return redirect("productos_menu")

    return render(request, "productos_eliminar.html", {
        "producto": producto
    })


# ------------------------------
# Menú de proveedores
# ------------------------------
@login_required
def proveedores_menu(request):
    opcion = request.GET.get("opcion", None)
    mensaje = None
    resultado = None

    # Formularios vacíos por defecto
    form_persona = ProveedorPersonaForm()
    form_empresa = ProveedorEmpresaForm()
    form_buscar = BuscarProveedorForm()

    # ---------------------------
    # Registrar Persona
    # ---------------------------
    if request.method == "POST" and opcion == "registrar_persona":
        form_persona = ProveedorPersonaForm(request.POST)
        if form_persona.is_valid():
            form_persona.save()
            messages.success(request, "✅ Proveedor Persona registrado correctamente.")
            return redirect("proveedores_menu")
        else:
            messages.error(request, "⚠️ Corrige los errores en el formulario de persona.")

    # ---------------------------
    # Registrar Empresa
    # ---------------------------
    if request.method == "POST" and opcion == "registrar_empresa":
        form_empresa = ProveedorEmpresaForm(request.POST)
        if form_empresa.is_valid():
            form_empresa.save()
            messages.success(request, "✅ Proveedor Empresa registrado correctamente.")
            return redirect("proveedores_menu")
        else:
            messages.error(request, "⚠️ Corrige los errores en el formulario de empresa.")

    # ---------------------------
    # Buscar Proveedor
    # ---------------------------
    if request.method == "POST" and opcion == "buscar":
        form_buscar = BuscarProveedorForm(request.POST)
        if form_buscar.is_valid():
            query = form_buscar.cleaned_data["query"]

            # Buscar primero en personas
            try:
                resultado = ProveedorPersona.objects.get(id_persona=query)
            except ProveedorPersona.DoesNotExist:
                try:
                    resultado = ProveedorEmpresa.objects.get(nit=query)
                except ProveedorEmpresa.DoesNotExist:
                    mensaje = "⚠️ No se encontró un proveedor con ese ID/NIT."
        else:
            mensaje = "⚠️ Por favor ingrese un valor válido."

    # ---------------------------
    # Lista de proveedores (activos y desactivos)
    # ---------------------------
    proveedores_personas = ProveedorPersona.objects.all()
    proveedores_empresas = ProveedorEmpresa.objects.all()

    return render(request, "proveedores_menu.html", {
        "opcion": opcion,
        "form_persona": form_persona,
        "form_empresa": form_empresa,
        "form_buscar": form_buscar,
        "resultado": resultado,
        "mensaje": mensaje,
        "proveedores_personas": proveedores_personas,
        "proveedores_empresas": proveedores_empresas,
    })


# ------------------------------
# Actualizar Proveedor Persona
# ------------------------------
@login_required
def actualizar_proveedor_persona(request, id_persona):
    proveedor = get_object_or_404(ProveedorPersona, id_persona=id_persona)
    if request.method == "POST":
        form = ProveedorPersonaForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Proveedor Persona actualizado con éxito.")
            return redirect("proveedores_menu")
    else:
        form = ProveedorPersonaForm(instance=proveedor)

    return render(request, "actualizar_proveedor_persona.html", {
        "form": form,
        "proveedor": proveedor
    })


# ------------------------------
# Actualizar Proveedor Empresa
# ------------------------------
@login_required
def actualizar_proveedor_empresa(request, nit):
    proveedor = get_object_or_404(ProveedorEmpresa, nit=nit)
    if request.method == "POST":
        form = ProveedorEmpresaForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Proveedor Empresa actualizado con éxito.")
            return redirect("proveedores_menu")
    else:
        form = ProveedorEmpresaForm(instance=proveedor)

    return render(request, "actualizar_proveedor_empresa.html", {
        "form": form,
        "proveedor": proveedor
    })


# ------------------------------
# Desactivar Proveedor Persona
# ------------------------------
@login_required
def proveedor_desactivar_persona(request, id_persona):
    proveedor = get_object_or_404(ProveedorPersona, id_persona=id_persona)
    if request.method == "POST":
        proveedor.activo = False
        proveedor.save()
        messages.success(request, "🚫 Proveedor Persona desactivado con éxito.")
        return redirect("proveedores_menu")

    return render(request, "proveedor_desactivar_persona.html", {
        "proveedor": proveedor,
        "tipo": "persona",
        "accion": "desactivar"
    })


# ------------------------------
# Desactivar Proveedor Empresa
# ------------------------------
@login_required
def proveedor_desactivar_empresa(request, nit):
    proveedor = get_object_or_404(ProveedorEmpresa, nit=nit)
    if request.method == "POST":
        proveedor.activo = False
        proveedor.save()
        messages.success(request, "🚫 Proveedor Empresa desactivado con éxito.")
        return redirect("proveedores_menu")

    return render(request, "proveedor_desactivar_empresa.html", {
        "proveedor": proveedor,
        "tipo": "empresa",
        "accion": "desactivar"
    })


# ------------------------------
# Reactivar Proveedor Persona
# ------------------------------
@login_required
def proveedor_reactivar_persona(request, id_persona):
    proveedor = get_object_or_404(ProveedorPersona, id_persona=id_persona)
    proveedor.activo = True
    proveedor.save()
    messages.success(request, "✅ Proveedor Persona reactivado con éxito.")
    return redirect("proveedores_menu")


# ------------------------------
# Reactivar Proveedor Empresa
# ------------------------------
@login_required
def proveedor_reactivar_empresa(request, nit):
    proveedor = get_object_or_404(ProveedorEmpresa, nit=nit)
    proveedor.activo = True
    proveedor.save()
    messages.success(request, "✅ Proveedor Empresa reactivado con éxito.")
    return redirect("proveedores_menu")

# ======================
# Menú de clientes (listar + registrar + buscar)
# ======================
@login_required
def clientes_menu(request):
    opcion = request.GET.get("opcion", "registrar")
    mensaje = None
    resultado = None

    # Registrar cliente
    if opcion == "registrar":
        if request.method == "POST":
            form = ClienteForm(request.POST)
            if form.is_valid():
                id_cliente = form.cleaned_data["id_cliente"]
                correo = form.cleaned_data["correo"]
                telefono = form.cleaned_data["telefono"]

                # Verificar duplicados por ID, correo o teléfono
                if Cliente.objects.filter(id_cliente=id_cliente).exists():
                    mensaje = "❌ Ya existe un cliente con ese ID."
                elif Cliente.objects.filter(correo=correo).exists():
                    mensaje = "❌ Ya existe un cliente con ese correo."
                elif Cliente.objects.filter(telefono=telefono).exists():
                    mensaje = "❌ Ya existe un cliente con ese teléfono."
                else:
                    form.save()
                    mensaje = "✅ Cliente registrado correctamente."
                    form = ClienteForm()  # limpiar formulario después de guardar
        else:
            form = ClienteForm()
        form_buscar = BuscarClienteForm()

    # Buscar cliente
    elif opcion == "buscar":
        if request.method == "POST":
            form_buscar = BuscarClienteForm(request.POST)
            if form_buscar.is_valid():
                busqueda = form_buscar.cleaned_data["busqueda"].strip()
                if busqueda == "":
                    mensaje = "⚠️ Ingresa un término para buscar."
                else:
                    qs1 = Cliente.objects.filter(id_cliente__icontains=busqueda)
                    qs2 = Cliente.objects.filter(nombre__icontains=busqueda)
                    qs3 = Cliente.objects.filter(primer_apellido__icontains=busqueda)
                    qs4 = Cliente.objects.filter(segundo_apellido__icontains=busqueda)
                    qs5 = Cliente.objects.filter(correo__icontains=busqueda)
                    qs6 = Cliente.objects.filter(telefono__icontains=busqueda)
                    resultado = (qs1 | qs2 | qs3 | qs4 | qs5 | qs6).distinct()
                    if not resultado.exists():
                        mensaje = "❌ No se encontraron clientes."
        else:
            form_buscar = BuscarClienteForm()
        form = ClienteForm()

    # Listado general de clientes (activos + inactivos para poder reactivar)
    clientes = Cliente.objects.all().order_by("id_cliente")

    return render(request, "clientes_menu.html", {
        "opcion": opcion,
        "mensaje": mensaje,
        "form": form,
        "form_buscar": form_buscar,
        "resultado": resultado,
        "clientes": clientes,
    })


# ======================
# Actualizar cliente
# ======================
@login_required
def actualizar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            correo = form.cleaned_data["correo"]
            telefono = form.cleaned_data["telefono"]

            # Validar duplicados (excluyendo el propio registro)
            if Cliente.objects.filter(correo=correo).exclude(id_cliente=id_cliente).exists():
                messages.error(request, "❌ Otro cliente ya utiliza ese correo.")
            elif Cliente.objects.filter(telefono=telefono).exclude(id_cliente=id_cliente).exists():
                messages.error(request, "❌ Otro cliente ya utiliza ese teléfono.")
            else:
                form.save()
                messages.success(request, "✅ Cliente actualizado correctamente.")
                return redirect("clientes_menu")
    else:
        form = ClienteForm(instance=cliente)
    return render(request, "actualizar_cliente.html", {"form": form, "cliente": cliente})


# ======================
# Desactivar cliente
# ======================
@login_required
def desactivar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    if request.method == "POST":
        cliente.activo = False
        cliente.save()
        messages.warning(request, f"🚫 Cliente {cliente.nombre} desactivado.")
        return redirect("clientes_menu")
    return render(request, "cliente_desactivar.html", {"cliente": cliente, "accion": "desactivar"})


# ======================
# Activar cliente
# ======================
@login_required
def activar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
    cliente.activo = True
    cliente.save()
    messages.success(request, f"✅ Cliente {cliente.nombre} activado.")
    return redirect("clientes_menu")