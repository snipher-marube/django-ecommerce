from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.products, name='products'),
    path('category/<slug:category_slug>/product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:category_slug>/', views.products, name='category_products'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('search/', views.search, name='search'),
]