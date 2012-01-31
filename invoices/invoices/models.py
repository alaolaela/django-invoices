#coding: utf-8
from __future__ import absolute_import

import re
from datetime import date

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from .. import settings


class Invoice(models.Model):
    SALE_TYPE_SERVICE = 1
    SALE_TYPE_COMMODITY = 2

    SALE_TYPE_CHOICES = (
        (SALE_TYPE_SERVICE, _(u'usługa')),
        (SALE_TYPE_COMMODITY, _(u'towar'))
    )

    STATUS_TOBEPAID = 1
    STATUS_OVERDUE = 2
    STATUS_DRAFT = 3
    STATUS_PAID = 4

    STATUS_CHOICES = (
        (STATUS_TOBEPAID, u'do zapłaty'),#_('to be paid')),
        (STATUS_OVERDUE, u'przeterminowane'),#_('overdue')),
        (STATUS_DRAFT, u'szkic'), #_('draft')),
        (STATUS_PAID, u'zapłacone') #_('paid')),

    )

    # the field may be changed by children-classes
    DEFAULT_STATUS = STATUS_DRAFT

    key = models.CharField(u'numer faktury', max_length=20, unique=True)
    date_created = models.DateField(u'data wystawienia')
    date_sale = models.DateField(u'data sprzedaży')
    date_payment = models.DateField(u'termin zapłaty')
    currency = models.PositiveSmallIntegerField(u'waluta', choices=settings.CURRENCIES,
            default=settings.PAYMENTS[0][0])
    payment_type = models.PositiveSmallIntegerField(u'sposób płatności', choices=settings.PAYMENTS, 
            default=settings.PAYMENTS[0][0])
    sale_type = models.PositiveSmallIntegerField(u'rodzaj sprzedaży', choices=SALE_TYPE_CHOICES,
            default=SALE_TYPE_SERVICE, null=True, blank=True)

    customer_content_type = models.ForeignKey(ContentType)
    customer_object_id = models.PositiveIntegerField(db_index=True)
    customer = generic.GenericForeignKey('customer_content_type',
            'customer_object_id')
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUS_CHOICES)

    class Meta:
        verbose_name = u'faktura'
        verbose_name = u'faktury'

    def __unicode__(self):
        return self.key
    
    def save(self, *args, **kwargs):
        if self.id and not self.key:
            self.key = self.generate_next_key()
            print self.key
        return super(Invoice, self).save(*args, **kwargs)

    @classmethod
    def generate_next_key(cls):
        month_key_invs = cls.objects.filter(key__regex=cls.KEY_PATTERN % {'num': '\d+',
            'month': date.today().strftime("%m"), 'year': date.today().strftime("%Y")})
        max_key = 0
        for inv in month_key_invs:
            key_index = re.match(cls.KEY_PATTERN_REGEX, inv.key).group(1)
            max_key = max(max_key, int(key_index))
        return cls.KEY_PATTERN % {'num': max_key + 1, 'month': date.today().strftime("%m"),
                'year': date.today().strftime("%Y")}

    @classmethod
    def validate_key(cls, key):
        return re.match(cls.KEY_PATTERN_REGEX, key) and \
                not cls.objects.filter(key__iexact=key).exists()


INVOICE_TYPE_VAT = 1
INVOICE_TYPE_PROFORMA = 2

class VatInvoice(Invoice):
    KEY_PATTERN = r'%(num)s/FV/%(month)s/%(year)s'
    KEY_PATTERN_REGEX = r'^%s$' % (KEY_PATTERN % {'num': '(\d+)', 'month': '[01][1-9]',
                                                  'year': '[0-9]{4}'})
    TYPE = INVOICE_TYPE_VAT

    class Meta:
        verbose_name  = u'faktura VAT'
        verbose_name_plural  = u'faktury VAT'

class ProformaInvoice(Invoice):
    KEY_PATTERN = r'%(num)s/PROF/%(month)s/%(year)s'
    KEY_PATTERN_REGEX = r'^%s$' % (KEY_PATTERN % {'num': '(\d+)', 'month': '[01][1-9]',
                                                  'year': '[0-9]{4}'})
    TYPE = INVOICE_TYPE_PROFORMA

    class Meta:
        verbose_name = u'faktura proforma'
        verbose_name_plural = u'faktury proforma'

    def __unicode__(self):
        return self.key

    @classmethod
    def generate_next_key(cls):
        return "P%s" % (super(cls, cls).generate_next_key())


INVOICE_TYPES = {
    INVOICE_TYPE_VAT: VatInvoice,
    INVOICE_TYPE_PROFORMA: ProformaInvoice
}

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
    net_price = models.FloatField(u'cena netto')
    tax = models.PositiveSmallIntegerField(choices=settings.TAXES, default=settings.TAXES[0][0])

    class Meta:
        verbose_name = u'pozycja faktury'
        verbose_name = u'pozycje faktury'

    def __unicode__(self):
        return u'%s - %s' % (self.invoice, self.product)

    @classmethod
    def get_for_autocomplete(cls, query):
        items = []
        for item in cls.objects.filter(name__icontains=query):
            items.append({
                'obj_id': item.product_object_id,
                'ct_id': item.product_content_type,
                'label': item.name,
                'desc': item.product.name if item.product else item.name,
            })
        return items
