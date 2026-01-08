import re
from django import template

register = template.Library()


@register.filter
def clean_phone_number(phone):
    if not phone:
        return ''
    return re.sub(r'\D', '', str(phone))


@register.filter
def format_phone_az(phone):
    
    if not phone:
        return ''
    digits = re.sub(r'\D', '', str(phone).strip())
    
    if not digits:
        return phone  
    
    if digits.startswith('994'):
        digits = digits[3:]
    
    if digits.startswith('0'):
        digits = digits[1:]
    
    if len(digits) > 9:
        digits = digits[-9:]
    
    if len(digits) != 9:
        return phone
    
    prefix = digits[:2]
    if prefix in {'50', '51', '55', '70', '77', '99'}:
        operator_code = digits[:2]  
        first_three = digits[2:5]   
        next_two = digits[5:7]      
        last_two = digits[7:9]      
        return f'+994 {operator_code} {first_three} {next_two} {last_two}'
    
    operator_code = digits[:2]
    first_three = digits[2:5]
    next_two = digits[5:7]
    last_two = digits[7:9]
    return f'+994 {operator_code} {first_three} {next_two} {last_two}'