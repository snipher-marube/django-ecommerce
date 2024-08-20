from django.urls import path

from . import views

urlpatterns = [
    path('payment/', views.payment, name='checkout'),
    path('success/', views.success, name='success'),
]