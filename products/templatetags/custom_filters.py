from django import template

register = template.Library()

@register.filter
def int_range(value):
    return range(int(value))
