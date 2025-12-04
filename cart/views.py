from django.contrib.auth import user_logged_in
from django.core.serializers import serialize
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


class AddToCartView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemsSerializers

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(buyer=request.user)
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

class UpdateCartView(generics.UpdateAPIView):
    serializer_class = CartItemsSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.get(buyer=self.request.user)
        return CartItems.objects.filter(cart=cart)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        change_amount_0 = request.data.get('quantity', 0)

        '''if not change_amount_0.isdigit():
            return Response({'detail': 'مقدار تغییر باید عددی باشد'}, status=status.HTTP_400_BAD_REQUEST)
        change_amount = int(change_amount_0)'''

        try:
            change_amount = int(change_amount_0)
        except (TypeError, ValueError):
            return Response(
                {'detail': 'مقدار باید عدد صحیح باشد'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not change_amount.is_integer():
                return Response({'detail': 'مقدار تغییر باید عددی باشد'}, status=status.HTTP_400_BAD_REQUEST)

        if change_amount > 10:
            return Response(
                {'detail': 'حداکثر تعداد ۱۰ عدد است'},
                status=status.HTTP_400_BAD_REQUEST)

        new_quantity = cart_item.quantity + change_amount

        if new_quantity <1 :
            cart_item.delete()
            return Response(
                {'detail': 'محصول شما از سبد خرید حذف شد'},
                status=status.HTTP_204_NO_CONTENT
            )

        if new_quantity > cart_item.product.inventory:
            return Response(
                {'detail': f'فقط {cart_item.product.inventory} عدد در انبار موجود است.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart_item.quantity = new_quantity
        cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

class RemoveCartItemsView(generics.DestroyAPIView):
    serializer_class = CartItemsSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.get(buyer=self.request.user)
        return CartItems.objects.filter(cart=cart)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {'detail': 'محصول از سبد خرید شما حذف شد'},
            status=status.HTTP_204_NO_CONTENT
        )

