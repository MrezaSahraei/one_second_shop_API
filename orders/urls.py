from django.urls import path


app_name = 'orders'
from . import views
urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='create_order'),

]