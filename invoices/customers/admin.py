#coding: utf-8
from __future__ import absolute_import

from django.contrib import admin

from .models import Customer


admin.site.register(Customer)
