#coding: utf-8
from __future__ import absolute_import

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from invoices import settings


class Invoice(models.Model):
    SALE_TYPES = (
        (1, _('service')),
        (2, _('commodity'))
    )

    key = models.CharField(max_length=20, unique=True)
    date_created = models.DateField()
    date_sale = models.DateField()
    date_payment = models.DateField()
    currency = models.PositiveSmallIntegerField(choices=settings.CURRENCIES)
    payment_type = models.PositiveSmallIntegerField(choices=settings.PAYMENTS)
    sale_type = models.PositiveSmallIntegerField(choices=SALE_TYPES)

    customer_content_type = models.ForeignKey(ContentType)
    customer_object_id = models.PositiveIntegerField(db_index=True)
    customer = generic.GenericForeignKey('customer_content_type',
            'customer_object_id')

    def __unicode__(self):
        return self.key


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, verbose_name='items')
    product_content_type = models.ForeignKey(ContentType)
    product_object_id =  models.PositiveIntegerField(db_index=True)
    product = generic.GenericForeignKey('product_content_type',
            'product_object_id')
    net_price = models.FloatField(null=True, blank=True)
    tax = models.PositiveSmallIntegerField(choices=settings.TAXES)
    amount = models.PositiveSmallIntegerField(default=1)

    def __unicode__(self):
        return u'%s - %s' % (self.invoice, self.product)
