from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import comentarios
from .models import Producto, Categoria

class ComentariosZForm(forms.ModelForm):
    
    ranking = forms.DecimalField(
        
        label='Ranking:',
        widget=forms.widgets.NumberInput(attrs={'type': 'range', 'step': '0.5', 'min': '0.0', 'max': '5.0'}),
        min_value=0.0,
        max_value=5.0
    )

    class Meta:
        model = comentarios
        fields = ['texto', 'ranking']

class CustomUserCreationForm(UserCreationForm):
     email = forms.EmailField
     password1 = forms.CharField(label='Contrasena', widget=forms.PasswordInput)
     password2 = forms.CharField(label='Confirmar Contrasena', widget=forms.PasswordInput)
     
     class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

class CrearProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'imagen', 'categoria', 'descripcion', 'precio']
        help_texts = {k:" " for k in fields}

class CrearCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        help_texts = {k:" " for k in fields}

class ProductoF(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['categoria', 'imagen', 'nombre', 'descripcion', 'precio']
        help_texts = {k:" " for k in fields}

class ProductSearchForm(forms.Form):
    query = forms.CharField(label='Buscar productos', max_length=100, required=False)
    category = forms.ModelChoiceField(queryset=Categoria.objects.all(), empty_label='Todas las categorías', required=False)

class CartShopForm(forms.Form):
    class Meta:
        model = Producto
        fields = ['product_id', 'nombre', 'precio', 'cantidad']
        help_texts = {k:" " for k in fields}

