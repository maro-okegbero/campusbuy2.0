from django import template


register = template.Library()

@register.filter(name = 'nigerianalize')

def nigerianalize(value):
    newvalue = value.strip('0')
    naija = "+234" + newvalue
    return naija















