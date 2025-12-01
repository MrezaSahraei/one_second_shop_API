from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    #Sending both parts to the front end
    ranges_price_display = serializers.CharField(source='get_ranges_price_display()', read_only=True)
    watch_genders_display = serializers.CharField(source='get_watch_genders_display', read_only=True)

    class Meta:
        model = Category
        fields = ['id',
                  'name',
                  'ranges_price',  #for POST/PUT/PATCH methods
                  'slug',
                  'watch_genders',  #for POST/PUT/PATCH methods
                  'ranges_price_display',
                  'watch_genders_display'
                  ]
        read_only_fields = ['id', 'slug']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo', 'description']
        read_only_fields = ['id', 'slug']

    def validate_name(self, value):
        if Brand.objects.filter(name__iexact=value).exists():  #none case-sensitive
            raise serializers.ValidationError('این برند از قبل وجود دارد')
        else:
            if Brand.objects.filter(name__iexact=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError('این برند از قبل وجود دارد')
        return value

class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    user_phone = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_phone','user_full_name', 'product',
                  'product_id', 'rating', 'comment', 'is_approved', 'created_at']

        read_only_fields = ['id', 'user', 'is_approved', 'created_at']

    def get_user_phone(self,obj):
        return obj.user.phone

    def get_user_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

