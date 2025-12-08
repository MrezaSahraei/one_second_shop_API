from django.shortcuts import render
from cart.models import Cart , CartItems
from .models import Order, OrderItems
from rest_framework. serializers import ValidationError
from .serializers import OrderSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import F
from rest_framework.response import Response
from django.db import transaction
# Create your views here.

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.get(buyer=user)

        cart_items = cart.cart_items.all()
        if not cart_items:

            return Response({'detail': 'سبد خرید شما خالی است'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vd = serializer.validated_data
        order = Order.objects.create(
            orderer=user,
            phone=vd['phone'],
            first_name=vd['first_name'],
            last_name=vd['last_name'],
            province=vd['province'],
            city=vd['city'],
            postal_code=vd['postal_code'],
            address=vd['address'],
            for_me=vd['for_you'],
            status='Pending',
            is_paid=False
        )

        for item in cart_items:
            if item.quantity > item.product.inventory:
                raise ValidationError(f'فقط {item.product.inventory} عدد در انبار موجود است.')

            OrderItems.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_now = item.product.price
            )
        cart_items.delete()

        return Response(
            {'order_id': order.id, 'detail': 'سفارش با موفقیت ثبت شد و در انتظار پرداخت است.'},
            status=status.HTTP_201_CREATED
        )

class BuyerOrdersListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(orderer=self.request.user)


