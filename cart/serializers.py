from rest_framework import serializers
from .models import *

class CartItemsSerializers(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.IntegerField(source='product.price', read_only=True)
    total_items_price = serializers.SerializerMethodField()
    formatted_price = serializers.SerializerMethodField()
    formatted_total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = [
            'id','product_id','product_name','product_price', 'quantity',
            'total_items_price', 'formatted_price', 'formatted_total_price'
        ]
        read_only_fields = ['id', 'product_price', 'product_name', 'total_items_price']

    def get_total_items_price(self, obj):
        return obj.total_items_price

    def get_formatted_price(self, obj):

        if obj.product.price  < 1000000:
            return f'{obj.product.price  / 1000:.0f} هزار تومان'
        else:
            return f'{obj.product.price / 1000000:.3f} میلیون تومان'

    def get_formatted_total_price(self, obj):
        total_price = obj.total_items_price

        if total_price < 1000000:
            return f'{total_price / 1000:.0f} هزار تومان'
        else:
            return f'{total_price / 1000000:.3f} میلیون تومان'

class CartSerializer(serializers.ModelSerializer):

    cart_items = CartItemsSerializers(many=True, read_only=True)
    total_cart_price = serializers.SerializerMethodField()
    formatted_total_cart_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'buyer', 'cart_items', 'total_cart_price', 'formatted_total_cart_price']
        read_only_fields = ['buyer', 'id']

    def get_total_cart_price(self,obj):
        return obj.total_cart_price

    def get_formatted_total_cart_price(self, obj):
        total_price = obj.total_cart_price
        if total_price < 1000000:
            return f'{total_price / 1000:.0f} هزار تومان'
        else:
            return f'{total_price / 1000000:.3f} میلیون تومان'

