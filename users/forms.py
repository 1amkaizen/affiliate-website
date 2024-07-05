# users/forms.py
from django import forms
from .models import UserProduct,UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm
from products.models import Category


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    company = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}))
    about = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About me'}), required=False)
    foto_profile = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'company', 'address', 'city', 'country', 'postal_code', 'about', 'foto_profile']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class UserProductForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Product Description'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select a category", widget=forms.Select(attrs={'class': 'form-control'}))
    affiliate_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Affiliate Link'}))
    image_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Opsional'}))
    image_file = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = UserProduct
        fields = ['name', 'description', 'price', 'category', 'affiliate_link', 'image_url', 'image_file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()







class EditProfileForm(UserChangeForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, required=False)
    postal_code = forms.CharField(max_length=20, required=False)
    company = forms.CharField(max_length=255100, required=False)
    about = forms.CharField(max_length=255, required=False)
    foto_profile = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'city', 'country', 'postal_code','company','about','foto_profile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Customize widgets or add additional initialization logic
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Address'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'City'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Country'})
        self.fields['postal_code'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Postal Code'})
        self.fields['company'].widget.attrs.update({'class': 'form-control', 'placeholder': 'company'})
        self.fields['about'].widget.attrs.update({'class': 'form-control', 'placeholder': 'about'})

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['city', 'address', 'country', 'postal_code', 'about', 'company', 'foto_profile']
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About me'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company'}),
            'foto_profile': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
