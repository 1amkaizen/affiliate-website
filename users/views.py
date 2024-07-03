# users/views.py

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserLoginForm, UserProductForm,EditProfileForm
from .models import UserProduct

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    context = {
        'ASSETS_ROOT': '/static/assets',
        'form': form,
    }
    return render(request, 'home/register.html', context)

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = UserLoginForm()
    
    context = {
        'ASSETS_ROOT': '/static/assets',
        'form': form,
    }
    return render(request, 'home/login.html', context)

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = UserProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('dashboard')
    else:
        form = UserProductForm()

    user_products = UserProduct.objects.filter(user=request.user)
    editing_product = request.GET.get('edit_product')

    context = {
        'ASSETS_ROOT': '/static/assets',
        'form': form,
        'user_products': user_products,
        'editing_product': int(editing_product) if editing_product else None
    }
    return render(request, 'home/index.html', context)

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(UserProduct, id=product_id, user=request.user)
    
    if request.method == 'POST':
        form = UserProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProductForm(instance=product)

    user_products = UserProduct.objects.filter(user=request.user)

    context = {
        'ASSETS_ROOT': '/static/assets',
        'form': form,
        'user_products': user_products,
        'editing_product': product_id
    }
    return render(request, 'home/edit_product.html', context)

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(UserProduct, id=product_id, user=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard')
    return render(request, 'home/dashboard.html', {'ASSETS_ROOT': '/static/assets'})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    context = {
        'ASSETS_ROOT': '/static/assets',
        'form': form,
    }

    return render(request, 'home/user.html', context)
