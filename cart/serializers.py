from rest_framework import serializers
from .models import *

class CartItemsSerializers(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.IntegerField(source='product.price', read_only=True)

    class Meta:
        model = CartItems
        fields = [
            'id','product','product_id','product_name','product_price', 'quantity',
        ]
        read_only_fields = ['id', 'product_price', 'product_name']

class CartSerializer(serializers.ModelSerializer):

    cart_items = CartItemsSerializers(many=True, read_only=True)
    total_cart_price = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = ['id', 'buyer', 'cart_items', 'total_cart_price']
        read_only_fields = ['buyer', 'id']


