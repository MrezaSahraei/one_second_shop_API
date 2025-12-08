from django.urls import path


app_name = 'orders'
from . import views
urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='create_order'),
    path('list/', views.BuyerOrdersListView.as_view(), name='orders_list'),


    #for admins or sellers
    path('list/admin', views.AdminsOrdersListView.as_view(), name='orders_list_for_admins')
]