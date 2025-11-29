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