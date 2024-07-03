# users/context_processors.py
from django.conf import settings

def assets_root(request):
    return {
        'ASSETS_ROOT': settings.ASSETS_ROOT,
    }

