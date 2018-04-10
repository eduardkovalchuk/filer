from django import template

register = template.Library()

@register.filter(name="get_field_value")
def get_field_value(dic, key):
    return dic[key]