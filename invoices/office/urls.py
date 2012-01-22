#coding: utf-8

from __future__ import absolute_import

from django.conf.urls import url, patterns

from .views import index 

urlpatterns = patterns('',
    url('^$', index)
)

