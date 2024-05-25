from django import template

register = template.Library()

@register.filter
def split_and_strip(value, delimiter=","):
    return [item.strip() for item in value.split(delimiter)]

@register.filter
def to_int(value):
    try:
        return int(value) if value else None
    except (ValueError, TypeError):
        return None

@register.filter
def map_to_int(value):
    return [int(item) for item in value if item.isdigit()]