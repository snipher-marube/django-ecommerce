from django.urls import path

from . import views

urlpatterns = [
    path('place-order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order-success/', views.success, name='order_success'),
]