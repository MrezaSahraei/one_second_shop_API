from django.db import models
from django.conf import settings
from accounts.models import ShopUser
from shop.models import Product
# Create your models here.

class Order(models.Model):
    STATUS_CHOICES= [
        ('Pending', 'در انتظار پرداخت'),
        ('Processing', 'در حال پردازش'),
        ('Shipped', 'ارسال شده'),
        ('Delivered', 'تحویل شده'),
        ('Canceled', 'لغو شده')
    ]
    PAYMENT_WAYS_CHOICES = [
        ('cash', 'نقدی در محل'),
        ('card', 'با کارت بانکی'),
    ]
    orderer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,related_name='orders', null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    #final_amount = models.PositiveIntegerField(default=0)
    address = models.TextField()
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=15)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending')
    pay_way = models.CharField(max_length=100, choices=PAYMENT_WAYS_CHOICES, default='card')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    for_you = models.BooleanField(default=False)
    discount_code = models.CharField(max_length=12, null=True)

    @property
    def final_order_price(self):
        total_order = 0
        for item in self.order_items.all():
            total_order += item.each_item_price
        if self.province == 'Tehran':
            return total_order + 50000
        return total_order + 100000


    def __str__(self):
        return f'order of {self.orderer}'

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, related_name='order_items', null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price_now = models.PositiveIntegerField(default=0)

    @property
    def each_item_price(self):
        return self.price_now * self.quantity

    def __str__(self):
        return f'{self.product} X {self.quantity}'





