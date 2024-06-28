# products/admin.py
from django.contrib import admin
from .models import Category, Ebook, Laptop, Gadget
from .forms import CsvUploadForm  # Import the form
import pandas as pd
from django.shortcuts import render, redirect
from django.urls import path
from datetime import datetime

class EbookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'price')
    change_list_template = "admin/products_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.upload_csv, name='ebook_upload_csv')
        ]
        return custom_urls + urls

    def parse_date(self, date_string):
        date_formats = [
            '%Y-%m-%d',   # 2024-03-25
            '%B %d, %Y',  # March 25, 2024
            '%d/%m/%Y',   # 25/03/2024
        ]
        for date_format in date_formats:
            try:
                return datetime.strptime(date_string, date_format).date()
            except (ValueError, TypeError):
                continue
        return None

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                self.message_user(request, "This is not a csv file")
                return redirect("..")

            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                try:
                    price_str = row['price'].replace('Rp ', '').replace('.', '').replace(',', '.')
                    price = float(price_str) if price_str else 0
                except (ValueError, TypeError):
                    price = 0  # or another default value

                try:
                    pages = int(float(row['jumlah halaman'])) if row['jumlah halaman'] else 0
                except (ValueError, TypeError):
                    pages = 0

                publication_date = self.parse_date(row['tanggal terbit']) if row['tanggal terbit'] else None

                ebook = Ebook(
                    name=row['title'] if pd.notnull(row['title']) else '',
                    author=row['author'] if pd.notnull(row['author']) else '',
                    price=price,
                    description=row['description'] if pd.notnull(row['description']) else '',
                    pages=pages,
                    publisher=row['penerbit'] if pd.notnull(row['penerbit']) else '',
                    publication_date=publication_date,
                    weight=float(row['berat']) if pd.notnull(row['berat']) else 0,
                    isbn=row['isbn'] if pd.notnull(row['isbn']) else '',
                    width=float(row['lebar']) if pd.notnull(row['lebar']) else 0,
                    language=row['bahasa'] if pd.notnull(row['bahasa']) else '',
                    length=float(row['panjang']) if pd.notnull(row['panjang']) else 0,
                    image_url=row['image_url'] if pd.notnull(row['image_url']) else '',
                    affiliate_link=row['affiliate_url'] if pd.notnull(row['affiliate_url']) else '',
                )
                category, created = Category.objects.get_or_create(name='Ebook')
                ebook.category = category
                ebook.save()
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        
        form = CsvUploadForm()
        context = {"form": form}
        return render(request, "admin/csv_form.html", context)






class LaptopAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price')
    change_list_template = "admin/products_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.upload_csv, name='laptop_upload_csv')
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                self.message_user(request, "This is not a csv file")
                return redirect("..")

            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                try:
                    price = float(row['price'].replace('Rp ', '').replace('.', '').replace(',', '.'))
                except ValueError:
                    price = 0  # or another default value
                laptop = Laptop(
                    name=row['title'],
                    brand=row['brand'] if pd.notnull(row['brand']) else '',
                    processor=row['processor'] if pd.notnull(row['processor']) else '',
                    ram=row['ram'] if pd.notnull(row['ram']) else '',
                    price=price,
                    description=row['description'] if pd.notnull(row['description']) else '',
                    image_url=row['image_url'] if pd.notnull(row['image_url']) else '',
                    affiliate_link=row['affiliate_url'] if pd.notnull(row['affiliate_url']) else '',
                )
                category, created = Category.objects.get_or_create(name='Laptop')
                laptop.category = category
                laptop.save()
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        
        form = CsvUploadForm()
        context = {"form": form}
        return render(request, "admin/csv_form.html", context)

class GadgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price')
    change_list_template = "admin/products_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.upload_csv, name='gadget_upload_csv')
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                self.message_user(request, "This is not a csv file")
                return redirect("..")

            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                try:
                    price = float(row['price'].replace('Rp ', '').replace('.', '').replace(',', '.'))
                except ValueError:
                    price = 0  # or another default value
                gadget = Gadget(
                    name=row['title'],
                    brand=row['brand'] if pd.notnull(row['brand']) else '',
                    features=row['features'] if pd.notnull(row['features']) else '',
                    price=price,
                    description=row['description'] if pd.notnull(row['description']) else '',
                    image_url=row['image_url'] if pd.notnull(row['image_url']) else '',
                    affiliate_link=row['affiliate_url'] if pd.notnull(row['affiliate_url']) else '',
                )
                category, created = Category.objects.get_or_create(name='Gadget')
                gadget.category = category
                gadget.save()
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        
        form = CsvUploadForm()
        context = {"form": form}
        return render(request, "admin/csv_form.html", context)

admin.site.register(Ebook, EbookAdmin)
admin.site.register(Laptop, LaptopAdmin)
admin.site.register(Gadget, GadgetAdmin)
admin.site.register(Category)

