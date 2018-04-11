from django import template


register = template.Library()


@register.filter
def int_to_css_colour(integer):
    return '#' + hex(integer)[2:]


@register.filter
def int_to_css_rgba(integer):
    r = (integer & 0xFF0000) >> 16
    g = (integer & 0xFF00) >> 8
    b = integer & 0xFF
    return f'rgba({r},{g},{b}, 0.15)'
