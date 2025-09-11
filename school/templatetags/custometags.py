from django import template

register = template.Library()

@register.filter(name='remplace')
def remplace(value):
    return value.replace(" ", "-")
