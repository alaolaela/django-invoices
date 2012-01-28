#coding: utf-8

from __future__ import absolute_import

from django.conf.urls import url, patterns

from .views import index, render_form, get_choices, products_search,\
        save_form, invoice_print

base_invoice = '^formsave/(?P<invoice_type>\d)/'
urlpatterns = patterns('',
    url('^$', index),
    url('^formtpl/(?P<invoice_type>\d)/$', render_form),
    url('%s$' % base_invoice, save_form),
    url('%s/(?P<invoice_id>\d+)$/' % base_invoice, save_form),
    url('^choices/(?P<ct_id>\d+)/$', get_choices),
    url('^products/$', products_search),
    url('^print/\.(?P<format>\w{2,4})$', invoice_print),
)

