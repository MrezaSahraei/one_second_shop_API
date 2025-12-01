from django.shortcuts import render
from .models import *
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import *
# Create your views here.

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CategoryRetrieve(generics.RetrieveAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class CategoryCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class CategoryUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class BrandList(generics.ListAPIView):
    queryset = Brand.objects.all().order_by('name')
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]

class BrandRetrieve(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class BrandCreate(generics.CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser]

class BrandUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser]

class ReviewsList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_slug = self.kwargs.get('slug')

        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'detail': 'محصول مورد نظر یافت نشد'})

        return Review.objects.filter(is_approved=True, product=product)


class ReviewsCreate(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        product_slug = self.kwargs.get('slug')
        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            raise serializers.ValidationError({'detail': 'محصول مورد نظر یافت نشد'})

        serializer.save(user=self.request.user, product=product)