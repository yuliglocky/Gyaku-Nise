from django.contrib import admin
from general.models import (Categoria,
    comentarios, Review,
    Producto )


@admin.register(Categoria)
class CatalogoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')

admin.site.register(comentarios)
admin.site.register(Review)



@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
# Register your models here.
