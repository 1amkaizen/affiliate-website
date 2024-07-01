# products/urls.py
from django.urls import path
from .views import product_list, product_detail,home,about,contact

urlpatterns = [
    path('', home, name='home'),
    path('product_list', product_list, name='product_list'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('category/<int:category_id>/', product_list, name='product_list_by_category'),
    path('product/<str:product_type>/<int:product_id>/', product_detail, name='product_detail'),
]

