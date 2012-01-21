#coding: utf-8
from __future__ import absolute_import

from django.contrib import admin

from invoices.models import Customer
from .models import Invoice, Product


for cls in (Invoice, Customer, Product):
    try:
        admin.site.register(cls)
    except admin.sites.AlreadyRegistered:
        pass
