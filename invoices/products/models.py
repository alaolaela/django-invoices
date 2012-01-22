#coding: utf-8
from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from invoices import settings


class Product(models.Model):

    name = models.CharField(max_length=200)
    net_price = models.PositiveIntegerField()
    tax = models.PositiveSmallIntegerField(choices=settings.TAXES)

    def __unicode__(self):
        return self.name
