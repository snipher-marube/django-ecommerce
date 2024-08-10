from django.urls import path

from . import views

urlpatterns = [
    path('my-cart/', views.cart,name='cart'),
    path('order/checkout/', views.checkout, name='checkout')
]