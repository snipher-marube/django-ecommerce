from django.urls import path

from . import views

urlpatterns = [
    path('all/', views.products, name='products'),
    path('product_detail/', views.product_detail, name='product_detail')
]