from django.db import models
from django.conf import settings
from shop.models import Product
# Create your models here.

class Cart(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts', null=True)
    session_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
            return f'cart of anonymous user'

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



