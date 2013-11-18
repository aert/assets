from django import template
from django.utils import translation
from django.utils.encoding import force_unicode


register = template.Library()


@register.simple_tag()
def next_lang():
    cur_language = translation.get_language()
    if cur_language == "fr":
        return "en"
    elif cur_language == "ar":
        return "fr"
    return "ar"

@register.filter('intchart')
def intchart(value):
    orig = force_unicode(value)
    new = orig.replace(",", ".")
    if orig == new:
        return new
    else:
        return intchart(new)
