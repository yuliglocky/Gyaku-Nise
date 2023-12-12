from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django.http import HttpResponse, HttpRequest
from django.db import IntegrityError
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate

from siz.settings import PAYPAL_RECEIVER_EMAIL
from .forms import CustomUserCreationForm

from  django.views import generic
def home(request):
	return render (request, 'general/home.html')

def index(request):
    if request.method == 'GET':
        return render(request, 'general/index.html', {"form": CustomUserCreationForm()})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user) #para crear una cookie xd
                return redirect('login')
            except IntegrityError:  #para manejar los intregacion de errores especificios de la base de datos 
                return render(request, 'general/index.html', {"form": CustomUserCreationForm, "error": "El usuario ya existe."})

        return render(request, 'general/index.html', {"form": CustomUserCreationForm, "error": "Contrasena no es la misma."})

def store(request):
     return render(request, 'general/productos.html')

def cerrar(request):
     logout(request)
     return render(request,'general/home.html')

def entrar(request):
    if request.method == 'GET':
        return render(request, 'general/login.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'general/login.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('vista')
    
from .forms import CrearProductoForm
from .models import Producto, comentarios, Categoria
from .forms import ProductoF
from .forms import ComentariosZForm

def crear_producto(request):
    if request.method == 'POST':
        form = CrearProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vista')  
    else:
        form = CrearProductoForm()
    return render(request, 'general/producto.html', {'form': form})



class listaView(generic.TemplateView):
	template_name = "general/vista.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
        
		productos = Producto.objects.all()
		categorias = Categoria.objects.all()
		
		context["productos"] = productos
		context["categorias"] = categorias
		return context


def actualizar(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = ProductoF(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('detalle', producto_id=producto_id)
    else:
        form = ProductoF(instance=producto)
    return render(request, 'general/actualizar.html', {'form': form})

#SECCION DE ELIMINAR PRODUCTO XD
def eliminar_produ(request, producto_id):
    producto = Producto.objects.get(pk=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('vista')  
    return render(request, 'general/vista.html', {'producto': producto})

#SECCION DE ELIMINAR CATEGORIA >:c
def eliminar_cate(request, categoria_id):
    categoria = Categoria.objects.get(pk=categoria_id)
    if request.method == 'POST':
        categoria.delete()
        return redirect('ver') 
    return render(request, 'general/vistacate.html', {'categoria': categoria})

#review de comentarios
def rate(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = ComentariosZForm(request.POST)
        if form.is_valid():
            nuevo_comentario = form.save(commit=False)
            nuevo_comentario.producto = producto
            nuevo_comentario.autor = request.user
            nuevo_comentario.save()
            return redirect('detalle', producto_id=producto_id)
    else:
        form = ComentariosZForm()
    return render(request, 'general/comentario.html', {'producto': producto, 'form': form})

def detalle(request, producto_id):
    producto = Producto.objects.get(pk=producto_id)
    related_products = Producto.objects.filter(categoria=producto.categoria).exclude(id=producto.id)[:3]
    
    comentario = comentarios.objects.filter(producto=producto)
    return render(request, 'general/detalle.html', {'producto': producto, 'comentarios': comentario, 'others': related_products})

#seccion de categoria 

from .forms import CrearCategoriaForm

def ver_categoria(request):
    categoria = Categoria.objects.all()
    return render(request, 'general/vistacate.html', {'categoria': categoria})

def crear_categoria(request):
    if request.method == 'POST':
        form = CrearCategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vista') 
    else:
        form = CrearCategoriaForm()
    return render(request, 'general/categoria.html', {'form': form})

def editar_categoria(request, categoria_id):
    categoria = Categoria.objects.get(pk=categoria_id)
    if request.method == 'POST':
        form = CrearCategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('vista') 
    else:
        form = CrearCategoriaForm(instance=categoria)
    return render(request, 'general/editar.html', {'form': form})


# busqueda de producto 
from .forms import ProductSearchForm

def search(request):
    if request.method == 'GET':
        form = ProductSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            category = form.cleaned_data['category']
            results = Producto.objects.all()

            if query:
                 results = results.filter(nombre__icontains=query)

            if category:
                results = results.filter(categoria=category)
        else:
            results = Producto.objects.all()
    else:
        form = ProductSearchForm()
        results = Producto.objects.all()

    return render(request, 'general/search.html', {'form': form, 'results': results})

#añadir a carrito
from .forms import CartShopForm

def añadir_carrito(request):
    if request.method == 'POST':
        form = CartShopForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('detalle')  
    else:
        form = CrearProductoForm()
    return render(request, 'general/detalle.html', {'form': form})

#paypal
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    # Obtener o inicializar la lista de productos en el carrito desde la sesión
    carrito = request.session.get('carrito', [])
    # Verificar si el producto ya está en el carrito
    for item in carrito:
        if item['id'] == producto.id:
            # Si el producto ya está en el carrito, puedes incrementar la cantidad
            item['cantidad'] += 1
            break
    else:
        # Si el producto no está en el carrito, añádelo con cantidad 1
        carrito.append({'id': producto.id, 'nombre': producto.nombre, 'precio': str(producto.precio), 'cantidad': 1})
    # Actualizar la sesión con la nueva lista de productos en el carrito
    request.session['carrito'] = carrito
    return redirect('product_search')


def ver_carrito(request):
    carrito = request.session.get('carrito', [])
    return render(request, 'general/ver_carrito.html', {'carrito': carrito})
def eliminar_del_carrito(request, producto_id):
    producto_id = int(producto_id)
    carrito = request.session.get('carrito', [])

    for i, item in enumerate(carrito):
        if item['id'] == producto_id:
            del carrito[i]
            break

    request.session['carrito'] = carrito
    return redirect('ver_carrito')


def calcular_total_carrito(self, productos_en_carrito):
     total = sum(producto.precio * producto.cantidad for producto in productos_en_carrito)
     return total

from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views import View
class PagoView(View):
    def obtener_productos_del_carrito(self, request):
        carrito = request.session.get('carrito', [])
        productos_en_carrito = []
        for producto_info in carrito:
            producto = Producto.objects.get(id=producto_info['id'])
            producto.cantidad = producto_info['cantidad']
            productos_en_carrito.append(producto)
        return productos_en_carrito

    def calcular_total_carrito(self, productos_en_carrito):
        total = sum(producto.precio * producto.cantidad for producto in productos_en_carrito)
        return total

    def get(self, request, *args, **kwargs):
        productos_en_carrito = self.obtener_productos_del_carrito(request)
        total_carrito = self.calcular_total_carrito(productos_en_carrito)

        paypal_dict = {
            "business": PAYPAL_RECEIVER_EMAIL,
            "amount": str(total_carrito),
            "item_name": "Descripción del pedido",
            "invoice": "id",  # Puedes usar un identificador único para cada pedido
            "currency_code": "USD",  # Ajusta la moneda según tu configuración
            "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
            "return_url": request.build_absolute_uri(reverse("pago_completado")),
            "cancel_return": request.build_absolute_uri(reverse("pago_cancelado")),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, "general/pago.html", {"form": form})
    
class PagoCanceladoView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'general/pago_cancelado.html')
    
from .models import pedido
class PagoCompletadoView(View):
    def obtener_productos_del_carrito(self, request):
        carrito = request.session.get('carrito', [])
        productos_en_carrito = []
        for producto_info in carrito:
            producto = Producto.objects.get(id=producto_info['id'])
            producto.cantidad = producto_info['cantidad']
            productos_en_carrito.append(producto)
        return productos_en_carrito

    def calcular_total_carrito(self, productos_en_carrito):
        total = sum(producto.precio * producto.cantidad for producto in productos_en_carrito)
        return total
    def get(self, request, *args, **kwargs): 
        # Obtener productos del carrito
        productos_en_carrito = self.obtener_productos_del_carrito(request)
        # Crear un nuevo pedido
        nuevo_pedido = pedido.objects.create(
            usuario=request.user,  # Asegúrate de que haya un usuario autenticado
            total=self.calcular_total_carrito(productos_en_carrito)
        )

        return render(request, 'general/pago_completado.html')
    

def obtener_informacion_carrito(request):
    carrito = request.session.get('carrito', [])
    return render(request, 'general/carrito_partial.html', {'carrito': carrito})

def vaciar_carrito(request):
    request.session['carrito'] = []
    if request.GET.get('pago_exitoso'):
        return redirect('pago_completado')
    return redirect('obtener_informacion_carrito')


class HistorialView(View):
    def get(self, request, *args, **kwargs):
        pedidos = pedido.objects.filter(usuario=request.user).order_by('-fecha')
        return render(request, 'general/historial.html', {'pedidos': pedidos})