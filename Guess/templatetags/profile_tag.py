from django import template

register = template.Library()

@register.simple_tag()
def sub(value1, value2):
    return value1-value2