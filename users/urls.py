# users/urls.py
from django.urls import path
from .views import register, user_login, user_logout, dashboard, edit_product, delete_product,edit_profile

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('edit-product/<int:product_id>/', edit_product, name='edit_product'),  # Tambahkan ini untuk edit product
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),  # Pastikan Anda memiliki ini juga
    path('edit-profile/', edit_profile, name='edit_profile'),
    ]


