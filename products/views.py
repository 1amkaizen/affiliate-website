import random
from django.shortcuts import render, get_object_or_404
from .models import Category, Ebook, Laptop, Gadget
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import (
    get_products_by_category, get_all_products, filter_products_by_query, 
    filter_products_by_price, filter_products_by_category, sort_products,
    get_random_products, get_latest_products
)

def product_list(request, category_id=None):
    query = request.GET.get('q')
    categories = Category.objects.all()

    # Ambil semua produk atau berdasarkan kategori
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        product_list = get_products_by_category(category)
    else:
        product_list = get_all_products()

    # Filtering dengan query pencarian
    if query:
        product_list = filter_products_by_query(product_list, query)

    # Ambil jumlah produk per halaman dari query string (default: 6)
    limit = int(request.GET.get('limit', 6))

    # Pengurutan berdasarkan pilihan pengguna
    sort = request.GET.get('sort')
    product_list = sort_products(product_list, sort)

    # Parsing filter dari query parameters
    min_price = float(request.GET.get('min_price', 0))
    max_price = float(request.GET.get('max_price', 500000))
    selected_categories = request.GET.get('categories', '').split(',')

    # Filter produk berdasarkan rentang harga
    product_list = filter_products_by_price(product_list, min_price, max_price)

    # Filter produk berdasarkan kategori
    product_list = filter_products_by_category(product_list, selected_categories)

    # Pagination dengan jumlah produk per halaman yang disesuaikan
    paginator = Paginator(product_list, limit)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Daftar produk teratas secara acak
    top_products = {
        'ebooks': get_random_products(Ebook, 3),
        'laptops': get_random_products(Laptop, 3),
        'gadgets': get_random_products(Gadget, 3),
    }

    # Daftar produk terbaru secara acak
    latest_products = {
        'ebooks': get_latest_products(Ebook, 3),
        'laptops': get_latest_products(Laptop, 3),
        'gadgets': get_latest_products(Gadget, 3),
    }

    # Daftar produk terkait secara acak (digunakan top_products untuk contoh)
    related_products = {
        'ebooks': get_random_products(Ebook, 3),
        'laptops': get_random_products(Laptop, 3),
        'gadgets': get_random_products(Gadget, 3),
    }

    # Kembalikan halaman dengan konteks yang diperlukan
    context = {
        'categories': categories,
        'products': products,
        'query': query,
        'top_products': top_products,
        'latest_products': latest_products,
        'related_products': related_products,
    }
    return render(request, 'products/product_list.html', context)


def home(request, category_id=None):
    categories = Category.objects.all()

    # Ambil produk terkait secara acak
    related_products = {
        'ebooks': get_random_products(Ebook, 12),
        'laptops': get_random_products(Laptop, 12),
        'gadgets': get_random_products(Gadget, 12),
    }

    # Ambil produk terbaru secara acak
    latest_products = {
        'ebooks': get_random_products(Ebook, 12),
        'laptops': get_random_products(Laptop, 12),
        'gadgets': get_random_products(Gadget, 12),
    }

    # Ambil produk teratas secara acak
    top_products = {
        'ebooks': get_random_products(Ebook, 12),
        'laptops': get_random_products(Laptop, 12),
        'gadgets': get_random_products(Gadget, 12),
    }

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = get_products_by_category(category)
    else:
        products = get_all_products()

    context = {
        'categories': categories,
        'products': products,
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
        related_products = get_random_products(Ebook, 3)
        latest_products = get_latest_products(Ebook, 3)
        top_products = get_random_products(Ebook, 3)

    elif product_type.lower() == 'laptop':
        product = get_object_or_404(Laptop, id=product_id)
        related_products = get_random_products(Laptop, 3)
        latest_products = get_latest_products(Laptop, 3)
        top_products = get_random_products(Laptop, 3)

    elif product_type.lower() == 'gadget':
        product = get_object_or_404(Gadget, id=product_id)
        related_products = get_random_products(Gadget, 3)
        latest_products = get_latest_products(Gadget, 3)
        top_products = get_random_products(Gadget, 3)

    context = {
        'product': product,
        'categories': categories,
        'related_products': related_products,
        'latest_products': latest_products,
        'top_products': top_products,
    }
    return render(request, 'products/product_detail.html', context)


def about(request):
    return render(request, 'products/about.html')


def contact(request):
    return render(request, 'products/contact.html')

