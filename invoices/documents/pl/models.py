#coding: utf-8
from __future__ import absolute_import

from django.db import models

from ...documents.models import InvoiceBase
from invoices.customers.models import CustomerBase
from invoices.products.models import ProductBase


class Invoice(InvoiceBase):
    abc = models.CharField(u'a', max_length=10)


class Customer(CustomerBase):
    pass


class Product(ProductBase):
    pass
