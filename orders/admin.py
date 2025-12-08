from django.contrib import admin
from .models import Order, OrderItems
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['orderer', 'province', 'status']

@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity']
