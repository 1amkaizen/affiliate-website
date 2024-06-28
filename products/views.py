# products/views.py
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Category, Ebook, Laptop, Gadget

def product_list(request, category_id=None):
    query = request.GET.get('q')
    categories = Category.objects.all()
    products = []

    if category_id:
        category = Category.objects.get(id=category_id)
        if category.name.lower() == 'ebook':
            products = Ebook.objects.filter(category_id=category_id)
        elif category.name.lower() == 'laptop':
            products = Laptop.objects.filter(category_id=category_id)
        elif category.name.lower() == 'gadget':
            products = Gadget.objects.filter(category_id=category_id)
    else:
        products = list(Ebook.objects.all()) + list(Laptop.objects.all()) + list(Gadget.objects.all())
    
    if query:
        products = [product for product in products if query.lower() in product.name.lower()]

    # Pagination
    paginator = Paginator(products, 8)  # Show 18 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products': page_obj,
        'query': query,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, product_id, product_type):
    product = None
    if product_type.lower() == 'ebook':
        product = get_object_or_404(Ebook, id=product_id)
    elif product_type.lower() == 'laptop':
        product = get_object_or_404(Laptop, id=product_id)
    elif product_type.lower() == 'gadget':
        product = get_object_or_404(Gadget, id=product_id)
    
    context = {
        'product': product
    }
    return render(request, 'products/product_detail.html', context)

