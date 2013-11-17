from django import template
from django.utils import translation


register = template.Library()


@register.simple_tag()
def next_lang():
    cur_language = translation.get_language()
    if cur_language == "fr":
        return "en"
    elif cur_language == "ar":
        return "fr"
    return "ar"
