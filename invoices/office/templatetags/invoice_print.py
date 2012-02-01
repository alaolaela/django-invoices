#coding: utf-8

from __future__ import absolute_import

from django import template
from django.utils import translation

register = template.Library()


@register.simple_tag
def trans_in(ln, text):
    cur_language = translation.get_language()
    translation.activate(ln)
    print unicode(text), translation.get_language()
    text = translation.ugettext(unicode(text))
    print ln, text
    translation.activate(cur_language)
    return text
