from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    CATEGORIES_BY_PRICE= (
    ('Economical-Level', 'اقتصادی' ),
    ('Mid-Range', 'میان رده' ),
    ('High-End', 'بالا رده')
    )
    CATEGORIES_BY_GENDER = (
        ('Men\'s', 'مردانه'),
        ('Women\'s', 'زنانه'),
        ('Unisex', 'اسپورت'),
    )
    name = models.CharField(max_length=255)
    ranges_price = models.CharField(max_length=20, choices=CATEGORIES_BY_PRICE, default='Mid-Range')
    slug = models.SlugField(max_length=255, unique=True)
    watch_genders = models.CharField(max_length=20, choices=CATEGORIES_BY_GENDER, default='Unisex')

    def __str__(self):
        return f'{self.name} - {self.get_watch_genders_display()}'

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORIES_BY_TYPE = (
        ('Quartz', 'کوارتز'),
        ('LCD', 'کامپیوتری'),
        ('Mechanical', 'مکانیکی'),
        ('Smart', 'هوشنمد')
    )

    CATEGORIES_BY_STRAP = (
        ('Buckle', 'سگکی'),
        ('Leather', 'چرمی'),
        ('Plastic', 'لاستیکی'),
    )
    CATEGORIES_BY_SHAPE = (
        ('Round', 'گرد'),
        ('Square', 'مربع'),
        ('Rectangle', 'مستطیلی'),
        ('Oval', 'بیضی')
    )
    CATEGORIES_BY_MATERIAL = (
        ('Stainless Steel', 'استیل ضد زنگ'),
        ('Titanium', 'تیتانیوم'),
        ('Gold Plated', 'با آبکاری طلا'),
        ('Plastic', 'پلاستیک'),
        ('Ceramic', 'سرامیک'),
    )

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    inventory = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0, help_text='به تومان')
    weight = models.PositiveIntegerField(default=0)
    off = models.PositiveIntegerField(default=0)
    #discount_price = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_waterproof = models.BooleanField(default=False)
    watch_type = models.CharField(max_length=20, choices=CATEGORIES_BY_TYPE, default='Quartz')
    watch_straps = models.CharField(max_length=20, choices=CATEGORIES_BY_STRAP, default='Buckle')
    watch_shapes = models.CharField(max_length=20, choices=CATEGORIES_BY_SHAPE, default='Round')
    watch_materials = models.CharField(max_length=20, choices=CATEGORIES_BY_MATERIAL, default='Stainless Steel')
    warranty = models.PositiveIntegerField(default=0, help_text='in months')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', 'brand']

    @property
    def discount_price(self):
        if self.off > 0:
            return self.price * (1 - self.off / 100)
        return self.price

    '''@property
    def main_image(self):
        return self.images.filter(is_main=True).first()'''

    def __str__(self):
        return f'{self.name}: {self.price}'

class GalleryProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    file = models.ImageField(upload_to="watch_images")
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'order']

    def save(self, *args, **kwargs):
        if self.is_main:
            GalleryProduct.objects.filter(product=self.product).update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} for {self.product}: {self.rating} stars'













