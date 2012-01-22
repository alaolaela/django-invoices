# -*- coding: utf-8 *-*
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


TAXES = getattr(settings, 'INVOICES_TAXES', ())

PAYMENTS = getattr(settings, 'INVOICES_PAYMENTS', (
    (1, _('bank transfer')),
    (2, _('cash')),
))

CURRENCIES = getattr(settings, 'INVOICES_CURRENCIES', ())

CUSTOMER_MODELS = getattr(settings, 'INVOICES_CUSTOMER_MODELS', ())

PRODUCT_MODELS = getattr(settings, 'INVOICES_PRODUCT_MODELS', ())
