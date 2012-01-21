#coding: utf-8
from __future__ import absolute_import

from . import settings

Customer = getattr(__import__('.'.join(settings.INVOICES_CUSTOMER.split('.')[:-1]),
            fromlist=[settings.INVOICES_CUSTOMER.split('.')[-2],]),
            settings.INVOICES_CUSTOMER.split('.')[-1])
