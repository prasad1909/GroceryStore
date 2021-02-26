from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="shopHome"),
    path('about/', views.about, name="aboutUs"),
    path('contact/', views.contact, name="contactUs"),
    path('tracker/', views.tracker, name="tracker"),
    path('products/<int:myid>', views.productView, name="productView"),
    path('checkOut/', views.checkOut, name="checkout"),
    path('search/',views.search, name="search")
]