# users/views.py

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserLoginForm, UserProductForm,EditProfileForm,EditUserProfileForm
from .models import UserProduct,UserProfile

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                city=form.cleaned_data.get('city', ''),
                address=form.cleaned_data.get('address', ''),
                country=form.cleaned_data.get('country', ''),
                postal_code=form.cleaned_data.get('postal_code', ''),
                about=form.cleaned_data.get('about', ''),
                foto_profile=request.FILES.get('foto_profile', None)
            )
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
    user_products = UserProduct.objects.filter(user=request.user)

    context = {
        'ASSETS_ROOT': '/static/assets',
        'user_products': user_products,
    }
    return render(request, 'home/index.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = UserProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('add_product')
    else:
        form = UserProductForm()

    user_products = UserProduct.objects.filter(user=request.user)

    context = {
        'ASSETS_ROOT': '/static/assets',
        'form': form,
        'user_products': user_products,
    }
    return render(request, 'home/tables.html', context)
@login_required
def edit_product(request, product_id):
    product = get_object_or_404(UserProduct, id=product_id, user=request.user)
    
    if request.method == 'POST':
        form = UserProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('add_product')
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
        return redirect('add_product')
    return render(request, 'home/dashboard.html', {'ASSETS_ROOT': '/static/assets'})

@login_required
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = EditUserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = EditUserProfileForm(instance=user_profile)

    context = {
        'ASSETS_ROOT': '/static/assets',
        'form': form,
        'profile_form': profile_form,
    }

    return render(request, 'home/user.html', context)

