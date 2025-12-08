from django.db import models
from django.db.models import F
from django.conf import settings
from shop.models import Product
from django.db import transaction
from django.db import IntegrityError
# Create your models here.

class Cart(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts', null=True)
    session_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


    @classmethod
    @transaction.atomic
    def merge_guest_cart(cls, user, session_key):
        try:
            guest_cart = cls.objects.get(session_id=session_key, buyer__isnull=True)
        except Cart.DoesNotExist:
            raise ValueError('سبد خرید یافت نشد')
        logged_in_user_cart, created = cls.objects.get_or_create(buyer=user, defaults={'session_id': None})

        for item in guest_cart.cart_items.all():
           try:
               existing_item = logged_in_user_cart.cart_items.get(product=item.product)
               existing_item.quantity =  F('quantity') + item.quantity
               existing_item.save()

           except CartItems.DoesNotExist:
               item.cart = logged_in_user_cart
               item.save()

        guest_cart.delete()

    @property
    def total_cart_price(self):
        total_cart = 0
        for item in self.cart_items.all():
            total_cart += item.total_items_price
        return total_cart

    def __str__(self):
        if self.buyer:
            return f'cart of {self.buyer.phone}'
        else:
            return f'guest user: {self.session_id}'

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    @property
    def total_items_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.name} X {self.quantity}'



