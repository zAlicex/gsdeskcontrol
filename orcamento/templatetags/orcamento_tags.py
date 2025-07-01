from django import template

register = template.Library()

@register.filter
def range_filter(number):
    return range(number) 