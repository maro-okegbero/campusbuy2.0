from django import template

register = template.Library()


@register.filter(name='nigerianalize')
def nigerianalize(value):
    if value[0] == "0":
        new_value = value.strip('0')
        niaja = "+234" + new_value
    else:
        niaja = value
    return niaja
