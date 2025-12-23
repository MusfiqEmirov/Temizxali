import re
from django import template

register = template.Library()


@register.filter
def clean_phone_number(phone):
    if not phone:
        return ''
    return re.sub(r'\D', '', str(phone))

