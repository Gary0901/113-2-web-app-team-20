from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """取得字典中的項目"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    return ''  # 如果不是字典，返回空字符串