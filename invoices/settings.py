# -*- coding: utf-8 *-*
from django.conf import settings


INVOICES_CUSTOMER = getattr(settings, 'INVOICES_CUSTOMER', None)
