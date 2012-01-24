#coding: utf-8

from __future__ import absolute_import

from django.conf.urls import url, patterns

from .views import index, render_form, get_choices

urlpatterns = patterns('',
    url('^$', index),
    url('^formtpl/$', render_form),
    url('^choices/(?P<ct_id>\d+)/$', get_choices)
)

