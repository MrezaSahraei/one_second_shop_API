from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from . models import Cart, CartItems, Product
from .serializers import CartSerializer, CartItemsSerializers
from rest_framework import status
from django.db import transaction
# Create your views here.

class CartRetrieveView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(buyer=self.request.user)
        return cart


class AddToCartVIew(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemsSerializers

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        cart= Cart.objects.get_or_create(buyer=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if  1> quantity or quantity > 10 :
            return Response(
                {'detail': 'تعداد باید بین ۱ تا ۱۰ باشد'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id, is_available=True)
        except Product.DoesNotExist:
            return Response(
                {'detail': 'محصول یافت نشد یا موجود نیست'},
                status=status.HTTP_404_NOT_FOUND
            )

        if product.inventory < quantity:
            #quantity = product.inventory
            return Response(
                {'detail': f'فقط {product.inventory} عدد در انبار موجود است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart_items, created = CartItems.objects.get_or_create(cart=cart, product=product, defaults={'quantity':quantity})
        if not created:
            all_quantity = cart_items.quantity + quantity
            cart_items.quantity = all_quantity

        cart_items.save()

        serializer = self.get_serializer(cart_items)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )