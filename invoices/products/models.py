#coding: utf-8
from __future__ import absolute_import

from django.db import models


class ProductBase(models.Model):

    name = models.CharField(u'name', max_length=200)

    class Meta:
        abstract = True
