from django.urls import path, include

from .views import CategoryCreate

app_name = 'shop'
from . import views
urlpatterns = [
    #for buyers
    #GET method for
    path('categories/', views.CategoryList.as_view(), name='categories_list'),

    path('categories/<slug:slug>', views.CategoryRetrieve.as_view(), name='category_detail'),

    path('brands/', views.BrandList.as_view(), name='brands_list'),

    path('brands/<slug:slug>', views.BrandRetrieve.as_view(), name='brands_detail'),


    #for admins or sellers
    #PUT, PATCH, DELETE:

    path('categories/create/', views.CategoryCreate.as_view(), name='category_create'),

    path('categories/update-destroy/<slug:slug>/', views.CategoryUpdateDestroy.as_view(), name='category_detail_update_destroy'),

    path('brands/create/', views.BrandCreate.as_view(), name='brand-create'),

    path('brands/update-destroy/<slug:slug>/',views.BrandUpdateDestroy.as_view(), name='brand_detail_update_destroy'),

    path('product/<slug:slug>/reviews', views.ReviewsList.as_view(), name='reviews'),

    path('product/<slug:slug>/review/create', views.ReviewsCreate.as_view(), name='review_create')
]