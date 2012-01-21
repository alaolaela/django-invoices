#coding: utf-8
from __future__ import absolute_import

from django.db import models

from invoices.models import Customer


class InvoiceBase(models.Model):

    customer = models.ForeignKey(Customer)

    class Meta:
        abstract = True

    def get_document_number(self):
        raise NotImplementedError
