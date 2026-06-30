# nebula/urls.py
from django.urls import path

from Eccomerce_Nebula_shop import settings
from django.conf.urls.static import static
from . import views

app_name = 'nebula'


urlpatterns = [ 

    # Rutas para Nebula_shop index, carrito, detalle 
    path('', views.index, name='index'), #Catalogo de productos
    path('carrito/', views.carrito, name='carrito'),
    path('product/<int:product_id>/', views.detalle, name='detalle'),
    path('product/<int:product_id>/add/', views.agregar_carrito, name='agregar_carrito'),
    path('product/<int:product_id>/remove/', views.quitar_carrito, name='quitar_carrito'),
    path('product/<int:product_id>/update/', views.actualizar_carrito, name='actualizar_carrito'),
    #Rutas para la gestión de productos           
    path('products/crud/', views.crud_view, name='crud'),
    path('products/', views.list_products, name='list_products'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/update/<int:product_id>/', views.update_product, name='update_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('products/list_products_update/', views.list_products_update, name='list_products_update'),
    path('products/list_products_delete/', views.list_products_delete, name='list_products_delete'),
    path('login/', views.login_view, name='login'),
    path('register_admin/', views.register_admin_user, name='register_admin_user'),
    path('logout/', views.logout_view, name='logout'),

    # Rutas para la gestión de categorías
    path('categories/', views.crud_categories, name='crud_categories'),
    path('categories/list', views.list_categories, name='list_categories'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/update/<int:category_id>/', views.update_category, name='update_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('categories/list_categories_update/', views.list_categories_update, name='list_categories_update'),
    path('categories/list_categories_delete/', views.list_categories_delete, name='list_categories_delete'),

    # Pago Exitoso
    path('realizar_pago/', views.realizar_pago, name='realizar_pago'),
    # Ruta crear orden de compra
    path('crear_orden/', views.create_order, name='crear_orden'),
    # Ruta ver ordenes del usuario autenticado
    path('ordenes/', views.view_orders, name='ver_ordenes'),
    # Ruta ver detalle de una orden
    path('ordenes/<int:order_id>/', views.order_detail, name='detalle_orden'),
    # Rutas para la gestión de usuarios
    path('register_customer/', views.register_customer, name='register_customer'),
    path('login_customer/', views.login_customer, name='login_customer'),
    path('logout_costumer/', views.logout_costumer, name='logout_costumer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   