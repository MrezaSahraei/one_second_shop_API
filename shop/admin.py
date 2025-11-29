from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'ranges_price', 'slug', 'watch_genders']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'logo', 'description']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['category', 'brand', 'name', 'slug', 'description',
              'inventory', 'price', 'weight', 'off', 'is_available',
              'is_waterproof', 'watch_type', 'watch_straps', 'watch_shapes',
              'watch_materials', 'warranty']

@admin.register(GalleryProduct)
class GalleryProductAdmin(admin.ModelAdmin):
    fields = ['product', 'file', 'description', 'is_main', 'order']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = ['user', 'product', 'rating', 'comment', 'is_approved']

