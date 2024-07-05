# users/models.py
from django.contrib.auth.models import User
from django.db import models
from products.models import Category
from django.utils import timezone

class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    affiliate_link = models.URLField(max_length=200)
    image_url = models.URLField(blank=True, null=True)
    image_file = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user_product_detail', args=[self.id])

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    about = models.TextField(blank=True)
    company = models.CharField(max_length=100, blank=True)
    foto_profile = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username
