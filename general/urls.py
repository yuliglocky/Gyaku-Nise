from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.ipn import views as paypal_ipn_views

urlpatterns = [

	path('', views.home, name="home"),
    #URL de register (cambiar el url xd que diga register)
    path('index/', views.index, name="register"),
    #URL de producto con su id respectivo
    path('producto/', views.crear_producto, name="producto"),
    path('producto/detalle/<int:producto_id>/', views.detalle, name='detalle'),
    path('producto/eliminar/<int:producto_id>/', views.eliminar_produ, name='eliminar_producto'),
    path('actualizar/<int:producto_id>/', views.actualizar, name='actualizar'),
    #seccion de comentario
    path('comentario/<int:producto_id>/', views.rate, name="comentario"),
    #Vista relacionada con categoria y producto
    path('vista/', views.listaView.as_view(), name="vista"),
    #url de logout
    path('logout/', views.cerrar, name="logout"),
    #URL de categoria con su id respectivo 
    path('categoria/editar/<int:categoria_id>/', views.editar_categoria, name='editar'),
    path('categoria/eliminar/<int:categoria_id>/', views.eliminar_cate, name='eliminar'),
    path('categoria/crear/', views.crear_categoria, name='crear'),
    path('categoria/', views.ver_categoria, name='ver'),
    #url de login 
    path('login/', views.entrar, name="login"), 
    #busqueda
    path('search/', views.search, name='product_search'),
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver-carrito/', views.ver_carrito, name='ver_carrito'),
    path('paypal/', views.ver_carrito, name='paypal'),
    path('pago/', views.PagoView.as_view(), name='pago'),
    path('pago/completado/', views.PagoCompletadoView.as_view(), name='pago_completado'),
    path('pago/cancelado/', views.PagoCanceladoView.as_view(), name='pago_cancelado'),
    path('paypal-ipn/', csrf_exempt(paypal_ipn_views.ipn), name='paypal-ipn'),
    path('vaciar_carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('eliminar-del-carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('historial/', views.HistorialView.as_view(), name='history'),
    path('obtener-informacion-carrito/', views.obtener_informacion_carrito, name='obtener_informacion_carrito'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)