#coding: utf-8
from __future__ import absolute_import

from django.contrib import admin

from .models import Product

admin.site.register(Product)
