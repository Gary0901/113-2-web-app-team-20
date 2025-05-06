from django.urls import path
from . import views

app_name = 'drink_shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('drinks/<str:category>/', views.category_detail, name='category_detail'),
    path('drink/<slug:drink_slug>/', views.drink_detail, name='drink_detail'),
    path('order/<uuid:order_id>/', views.order_status, name='order_status'),
]