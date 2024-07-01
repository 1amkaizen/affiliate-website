# products/utils.py
from .models import Category, Ebook, Laptop, Gadget

def get_products_by_category(category):
    if category.name.lower() == 'ebook':
        return Ebook.objects.filter(category=category)
    elif category.name.lower() == 'laptop':
        return Laptop.objects.filter(category=category)
    elif category.name.lower() == 'gadget':
        return Gadget.objects.filter(category=category)
    return []

def get_all_products():
    ebooks = list(Ebook.objects.all())
    laptops = list(Laptop.objects.all())
    gadgets = list(Gadget.objects.all())
    return ebooks + laptops + gadgets

def filter_products_by_query(products, query):
    return [product for product in products if query.lower() in product.name.lower()]

def filter_products_by_price(products, min_price, max_price):
    return [product for product in products if min_price <= product.price <= max_price]

def filter_products_by_category(products, selected_categories):
    if selected_categories and '' not in selected_categories:
        return [product for product in products if product.category.name in selected_categories]
    return products

def sort_products(products, sort):
    if sort == 'name_asc':
        return sorted(products, key=lambda x: x.name)
    elif sort == 'name_desc':
        return sorted(products, key=lambda x: x.name, reverse=True)
    elif sort == 'price_asc':
        return sorted(products, key=lambda x: x.price)
    elif sort == 'price_desc':
        return sorted(products, key=lambda x: x.price, reverse=True)
    elif sort == 'rating_desc':
        return sorted(products, key=lambda x: x.rating, reverse=True)
    elif sort == 'rating_asc':
        return sorted(products, key=lambda x: x.rating)
    elif sort == 'model_asc':
        return sorted(products, key=lambda x: x.model)
    elif sort == 'model_desc':
        return sorted(products, key=lambda x: x.model, reverse=True)
    return products

def get_random_products(model, count):
    return list(model.objects.order_by('?')[:count])

def get_latest_products(model, count):
    return list(model.objects.order_by('-created_at')[:count])

