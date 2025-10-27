from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import ProveedorForm, ProveedorPersonaForm, ProveedorEmpresaForm, ProductoForm, BuscarProductoForm, ActualizarProductoForm, BuscarProveedorForm, ClienteForm, BuscarClienteForm, FacturaCompraForm, DetalleCompraForm
from .models import Proveedor, ProveedorPersona, ProveedorEmpresa, Producto, Cliente, FacturaCompra, DetalleCompra, MovimientoInventario
from datetime import datetime

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
                codigo = form_registrar.cleaned_data["codigo"]

                # Verificar duplicado
                if Producto.objects.filter(codigo=codigo).exists():
                    mensaje = "❌ Ya existe un producto con ese código."
                else:
                    form_registrar.save()
                    mensaje = "✅ Producto registrado con éxito."
                    form_registrar = ProductoForm()  # Resetear formulario
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

    # Lista de productos (activos e inactivos)
    productos = Producto.objects.all().order_by("codigo")

    return render(request, "productos_menu.html", {
        "opcion": opcion,
        "form_registrar": form_registrar,
        "form_buscar": form_buscar,
        "resultado": resultado,
        "mensaje": mensaje,
        "productos": productos
    })


# ------------------------------
# Actualizar producto
# ------------------------------
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


# ------------------------------
# Desactivar producto
# ------------------------------
@login_required
def desactivar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    if request.method == "POST":
        producto.activo = False
        producto.save()
        messages.warning(request, f"🚫 Producto {producto.nombre} desactivado.")
        return redirect("productos_menu")
    return render(request, "producto_confirmar_estado.html", {
        "producto": producto,
        "accion": "desactivar"
    })


# ------------------------------
# Activar producto
# ------------------------------
@login_required
def activar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    producto.activo = True
    producto.save()
    messages.success(request, f"✅ Producto {producto.nombre} activado.")
    return redirect("productos_menu")

# ============================================================
# MENÚ PRINCIPAL DE PROVEEDORES (UNIFICADO)
# ============================================================

@login_required
def proveedores_menu(request):
    # pestaña activa por defecto
    opcion = request.GET.get("opcion", "registrar_persona")
    mensaje = None
    resultado = None

    # formularios por defecto
    form_persona = ProveedorPersonaForm()
    form_empresa = ProveedorEmpresaForm()
    form_buscar = BuscarProveedorForm()

    # ---------------------------
    # Registrar Persona
    # ---------------------------
    if request.method == "POST" and opcion == "registrar_persona":
        form_persona = ProveedorPersonaForm(request.POST)
        if form_persona.is_valid():
            persona = form_persona.save()
            # crear o actualizar entrada puente Proveedor
            prov, created = Proveedor.objects.get_or_create(
                persona=persona,
                defaults={"tipo": "persona", "activo": persona.activo}
            )
            if not created:
                prov.tipo = "persona"
                prov.activo = persona.activo
                prov.save()
            messages.success(request, "✅ Proveedor (persona) registrado correctamente.")
            return redirect("proveedores_menu")
        else:
            messages.error(request, "⚠️ Corrige los errores en el formulario de persona.")

    # ---------------------------
    # Registrar Empresa
    # ---------------------------
    elif request.method == "POST" and opcion == "registrar_empresa":
        form_empresa = ProveedorEmpresaForm(request.POST)
        if form_empresa.is_valid():
            empresa = form_empresa.save()
            # crear o actualizar entrada puente Proveedor
            prov, created = Proveedor.objects.get_or_create(
                empresa=empresa,
                defaults={"tipo": "empresa", "activo": empresa.activo}
            )
            if not created:
                prov.tipo = "empresa"
                prov.activo = empresa.activo
                prov.save()
            messages.success(request, "✅ Proveedor (empresa) registrado correctamente.")
            return redirect("proveedores_menu")
        else:
            messages.error(request, "⚠️ Corrige los errores en el formulario de empresa.")

    # ---------------------------
    # Buscar proveedor
    # ---------------------------
    elif request.method == "POST" and opcion == "buscar":
        form_buscar = BuscarProveedorForm(request.POST)
        if form_buscar.is_valid():
            q = form_buscar.cleaned_data["query"].strip()
            # buscar en la tabla puente para incluir ambos tipos
            resultado = Proveedor.objects.select_related("persona", "empresa").filter(
                Q(persona__id_persona__icontains=q) |
                Q(persona__nombre__icontains=q) |
                Q(persona__primer_apellido__icontains=q) |
                Q(empresa__nit__icontains=q) |
                Q(empresa__razon_social__icontains=q)
            )
            if not resultado.exists():
                mensaje = "⚠️ No se encontró un proveedor con ese ID/NIT o nombre."
        else:
            mensaje = "⚠️ Por favor ingrese un valor válido."

    # ---------------------------
    # Lista general de proveedores (usa la tabla puente)
    # ---------------------------
    proveedores = Proveedor.objects.select_related("persona", "empresa").all().order_by("tipo", "id")

    return render(request, "proveedores_menu.html", {
        "opcion": opcion,
        "form_persona": form_persona,
        "form_empresa": form_empresa,
        "form_buscar": form_buscar,
        "resultado": resultado,
        "mensaje": mensaje,
        "proveedores": proveedores,
    })

# ============================================================
# ACTUALIZAR PROVEEDOR
# ============================================================
@login_required
def actualizar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, pk=id)
    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Proveedor actualizado con éxito.")
            return redirect("proveedores_menu")
        else:
            messages.error(request, "⚠️ Corrige los errores en el formulario.")
    else:
        form = ProveedorForm(instance=proveedor)

    return render(request, "actualizar_proveedor.html", {
        "form": form,
        "proveedor": proveedor
    })


# ============================================================
# DESACTIVAR PROVEEDOR
# ============================================================
@login_required
def proveedor_desactivar(request, id):
    proveedor = get_object_or_404(Proveedor, pk=id)
    if request.method == "POST":
        proveedor.activo = False
        proveedor.save()
        messages.success(request, "🚫 Proveedor desactivado con éxito.")
        return redirect("proveedores_menu")

    return render(request, "proveedor_confirmar_accion.html", {
        "proveedor": proveedor,
        "accion": "desactivar"
    })


# ============================================================
# REACTIVAR PROVEEDOR
# ============================================================
@login_required
def proveedor_reactivar(request, id):
    proveedor = get_object_or_404(Proveedor, pk=id)
    proveedor.activo = True
    proveedor.save()
    messages.success(request, "✅ Proveedor reactivado con éxito.")
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

# ==========================================================
# 🧾 Registrar compra (actualiza stock y crea movimiento)
# ==========================================================
@login_required
def registrar_compra(request):
    if request.method == "POST":
        factura_form = FacturaCompraForm(request.POST)
        detalle_form = DetalleCompraForm(request.POST)

        if factura_form.is_valid() and detalle_form.is_valid():
            factura = factura_form.save()
            detalle = detalle_form.save(commit=False)
            detalle.factura = factura
            detalle.save()

            # ✅ Actualizar total de la factura
            factura.total += detalle.subtotal
            factura.save()

            # ============================================
            # 🧩 Registrar movimiento de inventario (ENTRADA)
            # ============================================
            producto = detalle.producto
            stock_anterior = producto.stock
            stock_nuevo = stock_anterior + detalle.cantidad

            MovimientoInventario.objects.create(
                producto=producto,
                tipo='ENTRADA',
                cantidad=detalle.cantidad,
                factura=factura,
                usuario=request.user,
                stock_anterior=stock_anterior,
                stock_nuevo=stock_nuevo,
                observacion=f"Compra registrada - Factura N° {factura.id}"
            )

            # ✅ Actualizar stock del producto
            producto.stock = stock_nuevo
            producto.save()

            messages.success(request, "✅ Compra registrada correctamente y stock actualizado.")
            return redirect("compras_menu")

    else:
        factura_form = FacturaCompraForm()
        detalle_form = DetalleCompraForm()

    return render(request, "compras_menu.html", {
        "factura_form": factura_form,
        "detalle_form": detalle_form,
    })

# ==========================================================
# 🧾 Gestión de facturas (registrar / consultar)
# ==========================================================
@login_required
def facturas_compra(request):
    opcion = request.GET.get("opcion", "registrar")

    # REGISTRAR FACTURA
    if opcion == "registrar":
        if request.method == "POST":
            form_factura = FacturaCompraForm(request.POST)
            form_detalle = DetalleCompraForm(request.POST)

            if form_factura.is_valid() and form_detalle.is_valid():
                factura = form_factura.save(commit=False)
                factura.usuario_registro = request.user
                factura.save()

                detalle = form_detalle.save(commit=False)
                detalle.factura = factura
                detalle.save()

                # ✅ Actualizar stock y registrar movimiento
                producto = detalle.producto
                stock_anterior = producto.stock
                stock_nuevo = stock_anterior + detalle.cantidad

                MovimientoInventario.objects.create(
                    producto=producto,
                    tipo='ENTRADA',
                    cantidad=detalle.cantidad,
                    factura=factura,
                    usuario=request.user,
                    stock_anterior=stock_anterior,
                    stock_nuevo=stock_nuevo,
                    observacion=f"Compra registrada - Factura #{factura.numero_factura}"
                )

                producto.stock = stock_nuevo
                producto.save()

                messages.success(request, "✅ Factura registrada y movimiento creado correctamente.")
                return redirect("facturas_compra")

        else:
            form_factura = FacturaCompraForm()
            form_detalle = DetalleCompraForm()

        return render(request, "facturas_compra_menu.html", {
            "opcion": opcion,
            "form_factura": form_factura,
            "form_detalle": form_detalle,
        })

    # CONSULTAR FACTURAS
    elif opcion == "consultar":
        facturas = FacturaCompra.objects.exclude(estado="anulada").order_by("-fecha_emision")
        return render(request, "facturas_compra_menu.html", {
            "opcion": opcion,
            "facturas": facturas,
        })

# ==========================================================
# 📄 Detalle de factura
# ==========================================================
@login_required
def factura_detalle(request, pk):
    factura = get_object_or_404(FacturaCompra, pk=pk)
    detalles = factura.detalles.all()
    return render(request, "detalle_factura.html", {"factura": factura, "detalles": detalles})

# ==========================================================
# ❌ Anular factura
# ==========================================================
@login_required
def anular_factura(request, pk):
    factura = get_object_or_404(FacturaCompra, pk=pk)

    if factura.estado == "anulada":
        messages.warning(request, f"La factura #{factura.numero_factura} ya está anulada.")
        return redirect("facturas_compra")

    # Revertir stock de los productos involucrados
    for detalle in factura.detalles.all():
        producto = detalle.producto
        producto.stock -= detalle.cantidad
        producto.save()

        # Marcar movimientos asociados como inactivos
        MovimientoInventario.objects.filter(factura=factura, producto=producto).update(activo=False)

    factura.estado = "anulada"
    factura.save()

    messages.success(request, f"Factura #{factura.numero_factura} anulada correctamente. Stock revertido.")
    return redirect("facturas_compra")

# ==========================================================
# 📋 Movimientos de inventario
# ==========================================================

@login_required
def movimientos_inventario(request):
    query_producto = request.GET.get("producto", "")
    fecha_desde = request.GET.get("fecha_desde", "")
    fecha_hasta = request.GET.get("fecha_hasta", "")

    movimientos = MovimientoInventario.objects.select_related(
        'producto', 'factura', 'usuario'
    ).order_by('-fecha')

    # Filtros dinámicos
    if query_producto:
        movimientos = movimientos.filter(producto__nombre__icontains=query_producto)

    # Filtro por rango de fechas
    if fecha_desde:
        try:
            fecha_inicio = datetime.strptime(fecha_desde, "%Y-%m-%d")
            movimientos = movimientos.filter(fecha__date__gte=fecha_inicio)
        except ValueError:
            pass

    if fecha_hasta:
        try:
            fecha_fin = datetime.strptime(fecha_hasta, "%Y-%m-%d")
            movimientos = movimientos.filter(fecha__date__lte=fecha_fin)
        except ValueError:
            pass

    context = {
        "movimientos": movimientos,
        "query_producto": query_producto,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
    }

    return render(request, "movimientos_inventario.html", context)
