from django.urls import path

from . import views

urlpatterns = [
    path('all/', views.products, name='products')
]