# products/views.py
import random

from django.shortcuts import render, get_object_or_404
from .models import Category, Ebook, Laptop, Gadget
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def product_list(request, category_id=None):
    query = request.GET.get('q')
    categories = Category.objects.all()
# Ambil produk teratas secara acak
    top_products = {
        'ebooks': list(Ebook.objects.order_by('?')[:3]),
        'laptops': list(Laptop.objects.order_by('?')[:3]),
        'gadgets': list(Gadget.objects.order_by('?')[:3]),
    }
    # Ambil produk terbaru secara acak
    latest_products = {
        'ebooks': list(Ebook.objects.order_by('?')[:3]),
        'laptops': list(Laptop.objects.order_by('?')[:3]),
        'gadgets': list(Gadget.objects.order_by('?')[:3]),
    }
    related_products = {
        'ebooks': list(Ebook.objects.order_by('?')[:3]),
        'laptops': list(Laptop.objects.order_by('?')[:3]),
        'gadgets': list(Gadget.objects.order_by('?')[:3]),
    }

    # Ambil semua produk
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        if category.name.lower() == 'ebook':
            product_list = Ebook.objects.filter(category=category)
        elif category.name.lower() == 'laptop':
            product_list = Laptop.objects.filter(category=category)
        elif category.name.lower() == 'gadget':
            product_list = Gadget.objects.filter(category=category)
    else:
        ebooks = Ebook.objects.all()
        laptops = Laptop.objects.all()
        gadgets = Gadget.objects.all()
        product_list = list(ebooks) + list(laptops) + list(gadgets)

    # Filtering dengan query pencarian
    if query:
        product_list = [product for product in product_list if query.lower() in product.name.lower()]

    # Pagination dengan 6 produk per halaman
    paginator = Paginator(product_list, 6)  # 6 produk per halaman
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Jika halaman tidak integer, tampilkan halaman pertama
        products = paginator.page(1)
    except EmptyPage:
        # Jika halaman di luar jangkauan (misalnya, halaman 9999), tampilkan halaman terakhir
        products = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'products': products,
        'query': query,
        'top_products': top_products,
        'latest_products': latest_products,
        'related_products': top_products,

    }
    return render(request, 'products/product_list.html', context)




def home(request, category_id=None):
    query = request.GET.get('q')
    categories = Category.objects.all()
    related_products = {
        'ebooks': list(Ebook.objects.order_by('?')[:12]),
        'laptops': list(Laptop.objects.order_by('?')[:12]),
        'gadgets': list(Gadget.objects.order_by('?')[:12]),
    }

    # Ambil produk terbaru secara acak
    latest_products = {
        'ebooks': list(Ebook.objects.order_by('?')[:12]),
        'laptops': list(Laptop.objects.order_by('?')[:12]),
        'gadgets': list(Gadget.objects.order_by('?')[:12]),
    }

    # Ambil produk teratas secara acak
    top_products = {
        'ebooks': list(Ebook.objects.order_by('?')[:12]),
        'laptops': list(Laptop.objects.order_by('?')[:12]),
        'gadgets': list(Gadget.objects.order_by('?')[:12]),
    }

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        if category.name.lower() == 'ebook':
            products = Ebook.objects.filter(category=category)
        elif category.name.lower() == 'laptop':
            products = Laptop.objects.filter(category=category)
        elif category.name.lower() == 'gadget':
            products = Gadget.objects.filter(category=category)
    else:
        ebooks = list(Ebook.objects.all())
        laptops = list(Laptop.objects.all())
        gadgets = list(Gadget.objects.all())
        products = ebooks + laptops + gadgets

    if query:
        products = [product for product in products if query.lower() in product.name.lower()]

    context = {
        'categories': categories,
        'products': products,
        'query': query,
        'latest_products': latest_products,
        'top_products': top_products,
        'related_products': top_products,

    }
    return render(request, 'products/home.html', context)



def product_detail(request, product_id, product_type):
    product = None
    categories = Category.objects.all()

    if product_type.lower() == 'ebook':
        product = get_object_or_404(Ebook, id=product_id)
        related_products = list(Ebook.objects.filter(category=product.category).exclude(id=product.id).order_by('?')[:3])
        latest_products = list(Ebook.objects.exclude(id=product.id).order_by('?')[:3])
        top_products = list(Ebook.objects.exclude(id=product.id).order_by('?')[:3])
        related_products = list(Ebook.objects.exclude(id=product.id).order_by('?')[:3])

    elif product_type.lower() == 'laptop':
        product = get_object_or_404(Laptop, id=product_id)
        related_products = list(Laptop.objects.filter(category=product.category).exclude(id=product.id).order_by('?')[:3])
        latest_products = list(Laptop.objects.exclude(id=product.id).order_by('?')[:3])
        top_products = list(Laptop.objects.exclude(id=product.id).order_by('?')[:3])
        related_products = list(Ebook.objects.exclude(id=product.id).order_by('?')[:3])

    elif product_type.lower() == 'gadget':
        product = get_object_or_404(Gadget, id=product_id)
        related_products = list(Gadget.objects.filter(category=product.category).exclude(id=product.id).order_by('?')[:3])
        latest_products = list(Gadget.objects.exclude(id=product.id).order_by('?')[:3])
        top_products = list(Gadget.objects.exclude(id=product.id).order_by('?')[:3])
        related_products = list(Ebook.objects.exclude(id=product.id).order_by('?')[:3])

    context = {
        'product': product,
        'categories': categories,
        'related_products': related_products,
        'latest_products': latest_products,
        'top_products': top_products,
    }
    return render(request, 'products/product_detail.html', context)

