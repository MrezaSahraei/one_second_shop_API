from django.urls import path, include


app_name = 'cart'
from . import views
urlpatterns = [
    path('cart/detail', views.CartRetrieveView.as_view(), name='cart_detail'),
    path('cart/add/', views.AddToCartVIew.as_view(), name='add_to_cart')

]