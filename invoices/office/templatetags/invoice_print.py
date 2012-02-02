#coding: utf-8

from __future__ import absolute_import

import threading
from django import template
from django.utils import translation

register = template.Library()
lock = threading.Lock()

@register.simple_tag
def trans_in(ln, text):
    lock.acquire()
    cur_language = translation.get_language()
    translation.activate(ln)
    text = unicode(text)
    translation.activate(cur_language)
    lock.release()
    return text
