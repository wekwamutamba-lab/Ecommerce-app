# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',                               views.home,             name='home'),
    path('products/',                      views.product_list,     name='product_list'),
    path('cart/',                          views.cart_view,        name='cart'),
    path('checkout/',                      views.checkout,         name='checkout'),
    path('add-to-cart/<int:product_id>/',  views.add_to_cart,      name='add_to_cart'),
    path('update-cart/<int:product_id>/',  views.update_cart,      name='update_cart'),
    path('remove/<int:product_id>/',       views.remove_from_cart, name='remove_from_cart'),
]