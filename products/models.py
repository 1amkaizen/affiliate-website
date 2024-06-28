# productss/models.py
from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    affiliate_link = models.URLField(max_length=200)
    image_url = models.URLField(blank=True, null=True)
    image_file = models.ImageField(upload_to='product_images/', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self._meta.model_name, self.id])

class Ebook(Product):
    author = models.CharField(max_length=200, default='Unknown Author')
    pages = models.IntegerField(default=0)
    publisher = models.CharField(max_length=200, default='Unknown Publisher')
    publication_date = models.DateField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    isbn = models.CharField(max_length=13, default='Unknown ISBN')
    width = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    language = models.CharField(max_length=100, default='Unknown Language')
    length = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)



class Laptop(Product):
    brand = models.CharField(max_length=100)
    processor = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)

class Gadget(Product):
    brand = models.CharField(max_length=100)
    features = models.TextField()
