from django.urls import path, include


app_name = 'cart'
from . import views
urlpatterns = [
    path('cart/detail', views.CartRetrieveView.as_view(), name='cart_detail'),

    path('cart/add/', views.AddToCartView.as_view(), name='add_to_cart'),

    path('cart/<int:pk>/update', views.UpdateCartView.as_view(), name='cart_update'),


]