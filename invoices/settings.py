# -*- coding: utf-8 *-*
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


TAXES = getattr(settings, 'INVOICES_TAXES', ())

PAYMENT_TRANSFER = 1
PAYMENT_CASH = 2
PAYMENTS = getattr(settings, 'INVOICES_PAYMENTS', (
    (PAYMENT_TRANSFER, _(u'przelew bankowy')),
    (PAYMENT_CASH, _(u'gotówka')),
))

CURRENCY_EUR = 1
CURRENCY_PLN = 2
CURRENCIES = getattr(settings, 'INVOICES_CURRENCIES', (
    (CURRENCY_EUR, _(u'EUR')),
    #(CURRENCY_PLN, _(u'PLN')),
    ))

CUSTOMER_MODELS = getattr(settings, 'INVOICES_CUSTOMER_MODELS', ())

PRODUCT_MODELS = getattr(settings, 'INVOICES_PRODUCT_MODELS', ())


PRINT_TYPE_ORIGINAL = 1
PRINT_TYPE_COPY = 2
PRINT_TYPE_DUPLICATED_ORIGINAL = 3
PRINT_TYPE_DUPLICATED_COPY = 4
PRINT_DOCUMENT_TYPES = (
    (PRINT_TYPE_ORIGINAL, u'Oryginał'),
    (PRINT_TYPE_COPY, u'Kopia'),
    (PRINT_TYPE_DUPLICATED_ORIGINAL, u'Duplikat oryginału'),
    (PRINT_TYPE_DUPLICATED_COPY, u'Duplikat kopii'),
)
