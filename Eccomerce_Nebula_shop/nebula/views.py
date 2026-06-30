from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django import forms
from django.shortcuts import redirect, render, get_object_or_404
from .models import OrderItem, Product, Category, Order, OrderItem
from django.contrib import messages
from django.shortcuts import render

#function-based y ORM, mas sistema de mensajes
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'image']  # Incluye el campo de imagen

# Formulario incio de sesion en panel personalizado
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
# Form para registrar nuevos usuarios con permisos de administrador bajo una clave maestra seteada por codigo
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    master_key = forms.CharField(widget=forms.PasswordInput, label='Clave maestra')

class register_customer_Form(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

# Helper para staff bloquear crud admin que no es superuser
def staff_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_staff)(view_func)
    return decorated_view_func

@staff_required
@permission_required('nebula.add_product', raise_exception=True)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return render(request, 'products/product_created.html', {'product': product})
        else:
            messages.error(request, 'Error al crear el producto. Por favor, verifica los datos ingresados.')
    else:
        form = ProductForm()

    categories = Category.objects.all()
    return render(request, 'products/create_product.html', {'form': form, 'categories': categories})

#CRUD Leer productos
@staff_required
@permission_required('nebula.view_product', raise_exception=True)
def list_products(request):
    products = Product.objects.all()
    return render(request, 'products/list_products.html', {'products': products})

#CRUD Actualizar producto
@staff_required
@permission_required('nebula.change_product', raise_exception=True)
def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return render(request, 'products/product_updated.html', {'product': product})
    else:
        form = ProductForm(instance=product)# se instancia el formulario con los datos del producto a actualizar
    categories = Category.objects.all()
    return render(request, 'products/update_product.html', {'form': form, 'categories': categories})

#CRUD Eliminar producto
@staff_required
@permission_required('nebula.delete_product', raise_exception=True)
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return render(request, 'products/product_deleted.html', {'product': product})
    else:
        return render(request, 'products/delete_product.html', {'product': product})

#Listar productos para actualizar
@staff_required
@permission_required('nebula.view_product', raise_exception=True)
def list_products_update(request):
    products = Product.objects.all()
    return render(request, 'products/list_products_update.html', {'products': products})
#Listar productos eliminar
@staff_required
@permission_required('nebula.view_product', raise_exception=True)
def list_products_delete(request):
    products = Product.objects.all()
    return render(request, 'products/list_products_delete.html', {'products': products})

#Vista para template crud.html
@staff_required
@permission_required('nebula.view_product', raise_exception=True)
def crud_view(request):
    return render(request, 'products/crud.html')

#Vista Inicio de sesion con auth y permiso de administrador con panel login personalizado
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Inicio de sesión exitoso.')
                return render(request, 'products/login_success.html', {'user': user})
                
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'products/login.html', {'form': form})

# Vista para registrar nuevos usuarios con permisos de administrador bajo una clave maestra
def register_admin_user(request):
    MASTER_KEY = 'modulo7'  # Clave maestra para registrar usuarios administradores

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            master_key = form.cleaned_data['master_key']

            if master_key == MASTER_KEY:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Ya existe un usuario con ese nombre.')
                    return render(request, 'products/register_admin.html', {'form': form})

                user = User.objects.create_user(username=username, password=password)
                user.is_staff = True  # Otorga permisos de administrador

                # Crear grupo Admins si no existe
                admins_group, created = Group.objects.get_or_create(name='Admins')

                # Permisos de Product
                ct = ContentType.objects.get_for_model(Product)
                permissions = Permission.objects.filter(
                    content_type=ct,
                    codename__in=[
                        'add_product',
                        'change_product',
                        'delete_product',
                        'view_product'
                    ]
                )

                # Permisos de Category
                ct_category = ContentType.objects.get_for_model(Category)
                permissions_category = Permission.objects.filter(
                    content_type=ct_category,
                    codename__in=[
                        'add_category',
                        'change_category',
                        'delete_category',
                        'view_category'
                    ]
                )

                # Asignar permisos al grupo Admins
                admins_group.permissions.add(*permissions)
                admins_group.permissions.add(*permissions_category)

                # Agregar usuario al grupo
                user.groups.add(admins_group)

                # Guardar usuario
                user.save()

                if created:
                    messages.success(request, 'Usuario administrador registrado exitosamente y grupo "Admins" creado automáticamente.')
                else:
                    messages.success(request, 'Usuario administrador registrado exitosamente y agregado al grupo "Admins".')

                return render(request, 'products/register_success.html', {'user': user})

            else:
                messages.error(request, 'Clave maestra incorrecta. No se puede registrar el usuario.')
        else:
            messages.error(request, 'Error al registrar el usuario. Verifica los datos ingresados.')
    else:
        form = RegisterForm()

    return render(request, 'products/register_admin.html', {'form': form})
# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente.')
    return render(request, 'products/logout_success.html')


# CRUD de Categorías
# Formulario para crear y actualizar categorías
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

# CRUD Crear categoría
@staff_required
@permission_required('nebula.add_category', raise_exception=True)
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return render(request, 'products/category_created.html', {'category': category})
        else:
            messages.error(request, 'Error al crear la categoría. Por favor, verifica los datos ingresados.')
    else:
        form = CategoryForm()
    return render(request, 'products/create_category.html', {'form': form})

# CRUD Leer categorías
@staff_required
@permission_required('nebula.view_category', raise_exception=True)
def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'products/list_categories.html', {'categories': categories})

# CRUD Actualizar categoría
@staff_required
@permission_required('nebula.change_category', raise_exception=True)
def update_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return render(request, 'products/category_updated.html', {'category': category})
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/update_category.html', {'form': form})

# CRUD Eliminar categoría
@staff_required
@permission_required('nebula.delete_category', raise_exception=True)
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return render(request, 'products/category_deleted.html', {'category': category})
    else:
        return render(request, 'products/delete_category.html', {'category': category})

# Listar categorías para actualizar
@staff_required
@permission_required('nebula.view_category', raise_exception=True)
def list_categories_update(request):
    categories = Category.objects.all()
    return render(request, 'products/list_categories_update.html', {'categories': categories})

# Listar categorías para eliminar
@staff_required
@permission_required('nebula.view_category', raise_exception=True)
def list_categories_delete(request):
    categories = Category.objects.all()
    return render(request, 'products/list_categories_delete.html', {'categories': categories})

#Vista crud_categories.html
@staff_required
@permission_required('nebula.view_category', raise_exception=True)
def crud_categories(request):
    categories = Category.objects.all()
    return render(request, 'products/crud_categories.html', {'categories': categories})

# Vistas para nebula_shop


# Create your views here.
def index(request):
    # Traer los productos para mostrarlos
    productos = Product.objects.all()
    return render(request, 'products/index.html', {'products': productos})
def carrito(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for item in cart.values():
        subtotal = item['price'] * item['quantity']
        total += subtotal
        item['subtotal'] = subtotal
        items.append(item)

    return render(request, 'products/carrito.html', {'items': items, 'total': total})


def agregar_carrito(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})

    product_key = str(product_id)
    if product_key in cart:
        cart[product_key]['quantity'] += 1
    else:
        cart[product_key] = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'stock': product.stock,
            'quantity': 1,
            'image': product.image.url if product.image else None,
        }

    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f'{product.name} agregado al carrito.')
    return redirect('nebula:carrito')

def quitar_carrito(request, product_id):
    cart = request.session.get('cart', {})
    key = str(product_id)

    if key in cart:
        del cart[key]

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('nebula:carrito')


def actualizar_carrito(request, product_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('quantity', 1))
        if cantidad < 1:
            cantidad = 1

        cart = request.session.get('cart', {})
        key = str(product_id)

        if key in cart:
            cart[key]['quantity'] = cantidad

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('nebula:carrito')

def detalle(request, product_id):
    # mostrar el detalle del producto
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detalle.html', {'product': product})

# # FUNCION DE COMO FUNCIONA EL SISTEMA DE REALIZAR PAGO Y DESCONTAR STOCK DE PRODUCTOS (No se implementa la pasarela de pagos solo se simula el proceso de pago y se descuenta el stock de los productos comprados)
def realizar_pago(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'El carrito está vacío. No se puede realizar el pago.')
        return redirect('nebula:carrito')

    # Simular el proceso de pago (aquí podrías integrar una pasarela de pagos real)
    # Por ahora, asumimos que el pago es exitoso

    # Descontar el stock de los productos comprados
    for item in cart.values():
        product_id = item['id']
        quantity = item['quantity']
        product = get_object_or_404(Product, pk=product_id)

        if product.stock >= quantity:
            product.stock -= quantity
            product.save()
        else:
            messages.error(request, f'No hay suficiente stock para {product.name}.')
            return redirect('nebula:carrito')

#     # Vaciar el carrito después del pago
    request.session['cart'] = {}
    request.session.modified = True

    messages.success(request, 'Pago realizado exitosamente. Gracias por su compra.')
    return render(request, 'products/pago_exitoso.html')

# Registro para un usuario cliente normal (no administrador) para poder realizar compras y tener un historial de pedidos.
def register_customer(request):
    if request.method == 'POST':
        form = register_customer_Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Ya existe un usuario con ese nombre.')
                return render(request, 'products/register_customer.html', {'form': form})

            user = User.objects.create_user(username=username, password=password)
            user.save()

            messages.success(request, 'Usuario registrado exitosamente. Ahora puede iniciar sesión.')
            return render(request, 'products/register_success_customer.html', {'user': user})
        else:
            messages.error(request, 'Error al registrar el usuario. Verifica los datos ingresados.')
    else:
        form = register_customer_Form()

    return render(request, 'products/register_customer.html', {'form': form})

# vista de login para clientes normales
def login_customer(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Inicio de sesión exitoso.')
                return render(request, 'products/login_success_customer.html', {'user': user})
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'products/login_customer.html', {'form': form})


# vista logout_costumer para clientes normales
def logout_costumer(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente.')
    return render(request, 'products/logout_success_customer.html')

# Vista para la orden creada por el cliente que mantiene sesion activa
# Esta vista cuando se acciona el boto de realizar pago crea una orden de compra para el usuario autenticado, asociando los productos del carrito a la orden y calculando el precio total. Luego, vacía el carrito, descuenta del stock y muestra un mensaje de éxito.
@login_required(login_url='/login_customer/')
def create_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'El carrito está vacío. No se puede crear la orden.')
        return redirect('nebula:carrito')

    # Calcular el precio total de la orden
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())

    # Crear la orden
    order = Order.objects.create(user=request.user, total_price=total_price)

    # Crear los items de la orden y descontar el stock
    for item in cart.values():
        product_id = item['id']
        quantity = item['quantity']
        product = get_object_or_404(Product, pk=product_id)

        if product.stock >= quantity:
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
            product.stock -= quantity
            product.save()
        else:
            messages.error(request, f'No hay suficiente stock para {product.name}.')
            order.delete()  # Eliminar la orden si no hay suficiente stock
            return redirect('nebula:carrito')

    # Vaciar el carrito después de crear la orden
    request.session['cart'] = {}
    request.session.modified = True

    messages.success(request, 'Orden creada exitosamente. Gracias por su compra.')
    return render(request, 'products/order_success.html', {'order': order})


# Vista para ver las ordenes del usuario autenticado, mostrando el detalle de cada orden y los productos asociados a ella.
@login_required(login_url='/login_customer/')
def view_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'products/view_orders.html', {'orders': orders})

# Vista para ver el detalle de una orden específica, mostrando los productos asociados a esa orden y sus cantidades.
# @login_required(login_url='/login_customer/')
# def order_detail(request, order_id):
#     order = get_object_or_404(Order, pk=order_id, user=request.user)
#     order_items = OrderItem.objects.filter(order=order)
#     return render(request, 'products/order_detail.html', {'order': order, 'order_items': order_items})



#Vista para ver el detalle de una orden específica, mostrando los productos asociados a esa orden y sus cantidades.
#Ademas suma el precio total de los productos en la orden y lo muestra en la plantilla.
@login_required(login_url='/login_customer/')
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)

    # Calcular el precio total de los productos en la orden
    total_price = sum(item.price * item.quantity for item in order_items)

    
    return render(request, 'products/order_detail.html', {'order': order, 'order_items': order_items, 'total_price': total_price})