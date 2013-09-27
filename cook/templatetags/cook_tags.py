from django import template
from django.conf import settings

register = template.Library()


def get_item(dictionary, key):
    return dictionary.get(key)
	
register.filter('get_item', get_item)

@register.simple_tag
def media_url():
    return settings.MEDIA_URL
