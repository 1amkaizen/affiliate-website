# products/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def format_rupiah(value):
    try:
        value = float(value)
        return f"Rp.{value:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return value

