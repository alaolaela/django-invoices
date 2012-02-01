#coding: utf-8

from __future__ import absolute_import

from django import template
from django.utils import translation

register = template.Library()


@register.simple_tag
def trans_in(ln, text):
    cur_language = translation.get_language()
    translation.activate(ln)
    text = translation.ugettext(unicode(text))
    translation.activate(cur_language)
    return text
