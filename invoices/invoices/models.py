#coding: utf-8
from __future__ import absolute_import

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from .. import settings


class Invoice(models.Model):
    SALE_TYPE_SERVICE = 1
    SALE_TYPE_COMMODITY = 2

    SALE_TYPES = (
        (SALE_TYPE_SERVICE, _(u'usługa')),
        (SALE_TYPE_COMMODITY, _(u'towar'))
    )

    STATUS_TOBEPAID = 1
    STATUS_OVERDUE = 2
    STATUS_DRAFT = 3
    STATUS_PAID = 4

    STATUS_CHOICES = (
        (STATUS_TOBEPAID, _('to be paid')),
        (STATUS_OVERDUE, _('overdue')),
        (STATUS_DRAFT, _('draft')),
        (STATUS_PAID, _('paid')),

    )

    key = models.CharField(max_length=20, unique=True)
    date_created = models.DateField(u'data wystawienia')
    date_sale = models.DateField(u'data sprzedaży')
    date_payment = models.DateField(u'termin zapłaty')
    currency = models.PositiveSmallIntegerField(u'waluta', choices=settings.CURRENCIES,
            default=settings.PAYMENTS[0][0])
    payment_type = models.PositiveSmallIntegerField(u'sposób płatności', choices=settings.PAYMENTS, 
            default=settings.PAYMENTS[0][0])
    sale_type = models.PositiveSmallIntegerField(u'rodzaj sprzedaży', choices=SALE_TYPES,
            default=SALE_TYPE_SERVICE, null=True, blank=True)

    customer_content_type = models.ForeignKey(ContentType)
    customer_object_id = models.PositiveIntegerField(db_index=True)
    customer = generic.GenericForeignKey('customer_content_type',
            'customer_object_id')
    status = models.PositiveSmallIntegerField(_('status'))

    def __unicode__(self):
        return self.key


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, verbose_name='items')
    name = models.TextField(u'nazwa')
    class_code = models.CharField(u'pkwiu', max_length=100)
    unit = models.CharField(u'jednostka miary', max_length=10)
    quantity = models.DecimalField(u'liczba/ilość', max_digits=8, decimal_places=2)
    product_content_type = models.ForeignKey(ContentType, null=True, blank=True)
    product_object_id =  models.PositiveIntegerField(db_index=True, null=True, blank=True)
    product = generic.GenericForeignKey('product_content_type',
            'product_object_id')
    net_price = models.FloatField(null=True, blank=True)
    tax = models.PositiveSmallIntegerField(choices=settings.TAXES)

    def __unicode__(self):
        return u'%s - %s' % (self.invoice, self.product)
