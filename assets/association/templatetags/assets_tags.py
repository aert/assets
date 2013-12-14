import base64
from django import template
from django.utils import translation
from django.utils.encoding import force_unicode
from django.conf import settings

import assets


register = template.Library()


@register.simple_tag()
def next_lang():
    cur_language = translation.get_language()
    if cur_language == "fr":
        return "en"
    #elif cur_language == "en":
    #    return "ar"
    return "fr"


@register.filter('intchart')
def intchart(value):
    orig = force_unicode(value)
    new = orig.replace(",", ".")
    if new == "0":
        return "null"
    if orig == new:
        return new
    else:
        return intchart(new)


@register.filter('amount')
def amount(value):
    orig = force_unicode(value)
    new = orig.replace(",", ".")
    if orig == new:
        return new
    else:
        return intchart(new)


@register.simple_tag()
def assets_version():
    return assets.VERSION


@register.simple_tag()
def tracking_code():
    code = settings.TRACKING_CODE
    if code:
        return base64.decodestring(code)
    return ""
