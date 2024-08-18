from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.products, name='products'),
    path('category/<slug:category_slug>/product/<slug:product_slug>/', views.product_detail, name='product_detail'),
]