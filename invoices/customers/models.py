#coding: utf-8
from __future__ import absolute_import

from django.db import models
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from invoices.documents.models import Invoice


class Customer(models.Model):

    name = models.CharField(_('name'), max_length=100)
    street = models.CharField(_('street'), max_length=50)
    post_code = models.CharField(_('post code'), max_length=6)
    city = models.CharField(_('city'), max_length=50)
    tin = models.CharField(_('tax identification number'), max_length=100,
            unique=True)
    phone_number = models.CharField(_('phone number'), max_length=20, null=True,
            blank=True)

    invoices = generic.GenericRelation(Invoice,
            object_id_field="customer_object_id")


    def __unicode__(self):
        return self.name
