import random
from django.shortcuts import render, get_object_or_404
from .models import Category, Ebook, Laptop, Gadget
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def product_list(request, category_id=None):
    query = request.GET.get('q')
    categories = Category.objects.all()

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

    # Ambil jumlah produk per halaman dari query string (default: 6)
    limit = int(request.GET.get('limit', 6))

    # Pengurutan berdasarkan pilihan pengguna
    sort = request.GET.get('sort')
    if sort == 'name_asc':
        product_list = sorted(product_list, key=lambda x: x.name)
    elif sort == 'name_desc':
        product_list = sorted(product_list, key=lambda x: x.name, reverse=True)
    elif sort == 'price_asc':
        product_list = sorted(product_list, key=lambda x: x.price)
    elif sort == 'price_desc':
        product_list = sorted(product_list, key=lambda x: x.price, reverse=True)
    elif sort == 'rating_desc':
        product_list = sorted(product_list, key=lambda x: x.rating, reverse=True)
    elif sort == 'rating_asc':
        product_list = sorted(product_list, key=lambda x: x.rating)
    elif sort == 'model_asc':
        product_list = sorted(product_list, key=lambda x: x.model)
    elif sort == 'model_desc':
        product_list = sorted(product_list, key=lambda x: x.model, reverse=True)

    # Parsing filter dari query parameters
    min_price = float(request.GET.get('min_price', 0))
    max_price = float(request.GET.get('max_price', 500000))
    selected_categories = request.GET.get('categories', '').split(',')

    # Filter produk berdasarkan rentang harga
    product_list = [product for product in product_list if min_price <= product.price <= max_price]

    # Filter produk berdasarkan kategori
    if selected_categories and '' not in selected_categories:
        product_list = [product for product in product_list if product.category.name in selected_categories]

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
        'ebooks': list(Ebook.objects.order_by('?')[:3]),
        'laptops': list(Laptop.objects.order_by('?')[:3]),
        'gadgets': list(Gadget.objects.order_by('?')[:3]),
    }

    # Daftar produk terbaru secara acak
    latest_products = {
        'ebooks': list(Ebook.objects.order_by('-created_at')[:3]),
        'laptops': list(Laptop.objects.order_by('-created_at')[:3]),
        'gadgets': list(Gadget.objects.order_by('-created_at')[:3]),
    }

    # Daftar produk terkait secara acak (digunakan top_products untuk contoh)
    related_products = {
        'ebooks': list(Ebook.objects.order_by('?')[:3]),
        'laptops': list(Laptop.objects.order_by('?')[:3]),
        'gadgets': list(Gadget.objects.order_by('?')[:3]),
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

def about(request):
    return render(request, 'products/about.html')

def contact(request):
    return render(request, 'products/contact.html')
