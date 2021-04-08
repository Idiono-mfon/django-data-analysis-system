from django import template
register = template.Library()


@register.filter(name='dict_value_or_null')
def dict_value_or_null(dict, key):
    if key in dict:
        return dict[key]
    else:
        return 'null'

@register.filter(name='array_value_or_null')
def array_value_or_null(list, key):
    if list[key] != '':
        return list[key]
    else:
        return 'null'

# @register.filter(name = replace_ng_with_npower)
# def replace_ng_with_npower(value, arg):
#     """Removes all values of arg from the given string"""
#     return value.replace(arg, 'Npower')