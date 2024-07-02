# affiliate_project/urls.py 

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
   # path('users/', include('users.urls')),
    path('', include('products.urls')),
]
# Menetapkan handler untuk halaman error 404
handler404 = 'affiliate_project.views.custom_404'
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

